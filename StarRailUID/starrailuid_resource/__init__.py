# ruff: noqa: RUF001
import asyncio
from collections.abc import Awaitable, Callable
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
import starrail_damage_cal.data_paths as srdc_data_paths
import starrail_damage_cal.excel.model
import starrail_damage_cal.map.SR_MAP_PATH  # noqa: F401 - load modules before refresh_loaded_data
import starrail_damage_cal.update as srdc_update

from .resource_status import inspect_data, inspect_icons, last_sync_summary, save_sync_result
from ..utils.excel.read_excel import update_light_cone_ranks
from ..utils.resource.RESOURCE_PATH import CHAR_ICON_PATH, MAIN_PATH, WEAPON_PATH
from ..utils.resource.download_all_file import check_use
from ..version import StarRailUID_version

sv_sr_download_config = SV("sr下载资源", pm=1)
sv_sr_resource_status = SV("sr资源状态")
_SYNC_RESULT_PATH = MAIN_PATH / "resource_sync_status.json"
ProgressCallback = Callable[[str], Awaitable[None]]
_RESOURCE_SYNC_LOCK = asyncio.Lock()


def _get_data_file_path(file_name: str) -> Path:
    relative_path = srdc_update.managed_relative_path(file_name)
    return srdc_data_paths.resolve_data_path(relative_path)


def _get_version_file_path() -> Path:
    return srdc_data_paths.resolve_version_file()


def _inspect_data():
    return inspect_data(
        _get_version_file_path(),
        _get_data_file_path,
        srdc_update.calc_sha256,
        srdc_update.SKIPPED_FILES,
    )


def _get_invalid_data_files() -> list[str]:
    return _inspect_data()[1]


def get_resource_status() -> str:
    try:
        dependency_version = version("starrail-damage-cal")
    except PackageNotFoundError:
        dependency_version = "未知"
    lines = [
        f"StarRailUID: {StarRailUID_version}",
        f"starrail-damage-cal: {dependency_version}",
    ]
    if _RESOURCE_SYNC_LOCK.locked():
        return "\n".join([*lines, "资源更新中；完成后可重新查询本地校验结果"])

    manifest, invalid, total = _inspect_data()
    data_version = manifest["version"] if manifest else "未知（版本清单缺失或损坏）"
    lines.extend(
        [
            f"运行数据版本: {data_version}",
            last_sync_summary(_SYNC_RESULT_PATH),
            f"数据校验: 共 {total}，异常 {len(invalid)}（本地版本清单 SHA256）"
            if manifest
            else "数据校验: 未检查（版本清单缺失或损坏）",
            inspect_icons("角色图标", _get_data_file_path("avatarId2Name_mapping.json"), CHAR_ICON_PATH),
            inspect_icons("光锥图标", _get_data_file_path("EquipmentID2Name_mapping.json"), WEAPON_PATH),
            "图片范围仅含当前核心映射中的角色、光锥图标；未联网检查最新版本。",
        ]
    )
    return "\n".join(lines)


@sv_sr_resource_status.on_fullmatch("资源状态")
async def send_resource_status(bot: Bot, ev: Event):
    await bot.send(get_resource_status())


def _invalidate_data_version_file() -> None:
    try:
        srdc_data_paths.runtime_path("version.json").unlink(missing_ok=True)
    except Exception:
        logger.exception("清理星铁数据版本文件失败")


async def _notify(progress: ProgressCallback | None, message: str) -> None:
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
    progress: ProgressCallback | None = None,
    *,
    silent: bool = False,
) -> list[str]:
    messages: list[str] = []
    async with _RESOURCE_SYNC_LOCK:
        stages: dict[str, str] = {}
        save_sync_result(_SYNC_RESULT_PATH, "running", stages)
        if not silent:
            await _notify(progress, "正在检查并同步资源文件")
        resource_ok = True
        try:
            resource_msg = await check_use()
        except Exception:
            logger.exception("同步资源文件时出错")
            resource_msg = "资源文件同步失败"
            resource_ok = False
        stages["图片资源"] = "success" if resource_ok else "failed"
        save_sync_result(_SYNC_RESULT_PATH, "running", stages)
        messages.append(resource_msg)
        logger.info(f"[sr资源同步] {resource_msg}")

        if not silent:
            await _notify(progress, "尝试更新数据文件")
        data_msg, data_ok = await _sync_data_files()
        stages["数据文件"] = "success" if data_ok else "failed"
        save_sync_result(_SYNC_RESULT_PATH, "running", stages)
        messages.append(data_msg)
        logger.info(f"[sr资源同步] {data_msg}")

        if not silent:
            await _notify(progress, "尝试更新光锥评价")
        try:
            light_cone_msg = await update_light_cone_ranks()
        except Exception:
            logger.exception("更新光锥评价时出错")
            light_cone_msg = "光锥评价更新失败"
        ranks_ok = light_cone_msg in {"光锥评价数据已是最新版本", "光锥评价已更新并重新加载"}
        stages["光锥评价"] = "success" if ranks_ok else "failed"
        save_sync_result(_SYNC_RESULT_PATH, "running", stages)
        messages.append(light_cone_msg)
        logger.info(f"[sr资源同步] {light_cone_msg}")

        if data_ok:
            reload_msg = await _reload_data_modules()
            stages["数据刷新"] = "success" if reload_msg.startswith("✅") else "failed"
            messages.append(reload_msg)
            logger.info(f"[sr资源同步] {reload_msg}")

        result = "failed" if "failed" in stages.values() else "success"
        save_sync_result(_SYNC_RESULT_PATH, result, stages)

    return messages


@sv_sr_download_config.on_fullmatch("下载全部资源")
async def send_download_resource_msg(bot: Bot, ev: Event):
    await bot.send("sr正在开始下载~可能需要较久的时间!")
    for message in await sync_all_resources(bot.send):
        await bot.send(message)


async def startup():
    logger.info("[sr资源同步] 启动时开始检查资源与数据更新")
    await sync_all_resources(silent=True)
