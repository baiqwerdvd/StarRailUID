import asyncio
import json
from pathlib import Path
from typing import Awaitable, Callable, Optional

from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
import starrail_damage_cal.data_paths as srdc_data_paths
import starrail_damage_cal.excel.model
import starrail_damage_cal.map.SR_MAP_PATH
import starrail_damage_cal.update as srdc_update

from ..utils.excel.read_excel import update_light_cone_ranks
from ..utils.resource.download_all_file import check_use

sv_sr_download_config = SV("sr下载资源", pm=1)
ProgressCallback = Callable[[str], Awaitable[None]]
_RESOURCE_SYNC_LOCK = asyncio.Lock()


def _get_data_file_path(file_name: str) -> Path:
    relative_path = srdc_update.managed_relative_path(file_name)
    return srdc_data_paths.resolve_data_path(relative_path)


def _get_version_file_path() -> Path:
    return srdc_data_paths.resolve_version_file()


def _get_invalid_data_files() -> list[str]:
    version_file = _get_version_file_path()
    if not version_file.exists():
        return [version_file.name]

    try:
        version_data = json.loads(version_file.read_text(encoding="utf-8"))
    except Exception:
        logger.exception("读取星铁数据版本文件失败")
        return [version_file.name]

    invalid_files: list[str] = []
    files = version_data.get("files", {})
    for file_name in version_data.get("file_names", []):
        if file_name in srdc_update.SKIPPED_FILES:
            continue

        file_info = files.get(file_name, {})
        expected_sha = file_info.get("sha256") if isinstance(file_info, dict) else None
        if not expected_sha:
            invalid_files.append(file_name)
            continue

        path = _get_data_file_path(file_name)
        if not path.exists():
            invalid_files.append(file_name)
            continue

        if srdc_update.calc_sha256(path) != expected_sha:
            invalid_files.append(file_name)

    return invalid_files


def _invalidate_data_version_file() -> None:
    try:
        srdc_data_paths.runtime_path("version.json").unlink(missing_ok=True)
    except Exception:
        logger.exception("清理星铁数据版本文件失败")


async def _notify(progress: Optional[ProgressCallback], message: str) -> None:
    if progress is not None:
        await progress(message)


async def _sync_data_files() -> tuple[str, bool]:
    for attempt in range(2):
        try:
            result = await srdc_update.update_resource()
        except Exception:
            logger.exception("更新星铁数据文件时出错")
            _invalidate_data_version_file()
            return "数据文件更新失败", False

        invalid_files = _get_invalid_data_files()
        if not invalid_files:
            if attempt == 1:
                return f"{result}（检测到文件不一致后已自动重试）", True
            return result, True

        logger.warning(f"[sr资源同步] 星铁数据文件校验失败: {', '.join(invalid_files[:10])}")
        _invalidate_data_version_file()

    preview = "、".join(_get_invalid_data_files()[:3]) or "未知文件"
    return f"⚠️ 数据文件校验未通过，请稍后重试。异常文件: {preview}", False


async def _reload_data_modules() -> str:
    try:
        srdc_update.refresh_loaded_data()
    except Exception:
        logger.exception("刷新数据时出错")
        return "⚠️ 数据刷新可能发生异常，建议重新启动以重载数据"
    return "✅ 数据模块已刷新"


async def sync_all_resources(
    progress: Optional[ProgressCallback] = None,
    *,
    silent: bool = False,
) -> list[str]:
    messages: list[str] = []
    async with _RESOURCE_SYNC_LOCK:
        if not silent:
            await _notify(progress, "正在检查并同步资源文件")
        try:
            resource_msg = await check_use()
        except Exception:
            logger.exception("同步资源文件时出错")
            resource_msg = "资源文件同步失败"
        messages.append(resource_msg)
        logger.info(f"[sr资源同步] {resource_msg}")

        if not silent:
            await _notify(progress, "尝试更新数据文件")
        data_msg, data_ok = await _sync_data_files()
        messages.append(data_msg)
        logger.info(f"[sr资源同步] {data_msg}")

        if not silent:
            await _notify(progress, "尝试更新光锥评价")
        try:
            light_cone_msg = await update_light_cone_ranks()
        except Exception:
            logger.exception("更新光锥评价时出错")
            light_cone_msg = "光锥评价更新失败"
        messages.append(light_cone_msg)
        logger.info(f"[sr资源同步] {light_cone_msg}")

        if data_ok:
            reload_msg = await _reload_data_modules()
            messages.append(reload_msg)
            logger.info(f"[sr资源同步] {reload_msg}")

    return messages


@sv_sr_download_config.on_fullmatch("下载全部资源")
async def send_download_resource_msg(bot: Bot, ev: Event):
    await bot.send("sr正在开始下载~可能需要较久的时间!")
    for message in await sync_all_resources(bot.send):
        await bot.send(message)


async def startup():
    logger.info("[sr资源同步] 启动时开始检查资源与数据更新")
    await sync_all_resources(silent=True)
