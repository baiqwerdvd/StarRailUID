import asyncio
from datetime import datetime, timedelta, timezone
import json
from typing import TypedDict

import aiofiles
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.utils.database.models import GsUser

from .storage import refresh_lock, write_json_atomic
from ..utils.mys_api import mys_api
from ..utils.resource.RESOURCE_PATH import PLAYER_PATH

POOL_MAP: dict[str, tuple[str, str]] = {
    "群星跃迁": ("GachaType_Standard", "1"),
    "始发跃迁": ("GachaType_Newbie", "2"),
    "角色跃迁": ("GachaType_AvatarUp", "11"),
    "光锥跃迁": ("GachaType_EquipmentUp", "12"),
    "角色联动跃迁": ("GachaType_CollabAvatarUp", "21"),
    "光锥联动跃迁": ("GachaType_CollabEquipmentUp", "22"),
}


class GachaItemInfo(TypedDict):
    item_id: int
    name: str
    icon: str
    item_type: str
    rarity: int
    big_icon: str


class RawGachaRecord(TypedDict):
    item: GachaItemInfo | None
    is_up: bool
    got_item: bool
    gacha_count: int
    uuid: str
    id: str


class SingleGachaRecord(TypedDict):
    uid: str
    gacha_id: str
    gacha_type: str
    item_id: str
    count: str
    time: str
    name: str
    lang: str
    item_type: str
    rank_type: str
    id: str
    gacha_count: int
    is_up: bool


class GachaLogsData(TypedDict):
    uid: str
    data_time: str
    normal_gacha_num: int
    begin_gacha_num: int
    char_gacha_num: int
    weapon_gacha_num: int
    char_collabo_gacha_num: int
    weapon_collabo_gacha_num: int
    pity_counts: dict[str, int]
    pool_data_time: dict[str, str]
    data: dict[str, list[SingleGachaRecord]]


def _timestamp_to_time_str(raw_id: str) -> str:
    if len(raw_id) >= 10 and raw_id[:10].isdigit():
        ts = int(raw_id[:10])
        # 东八区时间
        tz = timezone(timedelta(hours=8))
        dt = datetime.fromtimestamp(ts, tz=tz)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return ""


async def _fetch_pool_records(
    uid: str,
    cookie: str,
    device_id: str,
    gacha_type_code: str,
    gacha_type_id: str,
    is_force: bool = False,
    latest_id: str | None = None,
) -> tuple[list[SingleGachaRecord], int] | None:
    records: list[SingleGachaRecord] = []
    pity_count: int | None = None
    saw_records = False
    next_max_id: str | None = None
    version_id: str | None = None
    has_more = True
    stop_pagination = False

    while has_more and not stop_pagination:
        res = await mys_api.get_gacha_five_star_list(
            uid=uid,
            cookie=cookie,
            gacha_type=gacha_type_code,
            device_id=device_id,
            max_id=next_max_id,
            version_id=version_id,
        )
        if not isinstance(res, dict) or res.get("retcode") != 0:
            logger.warning(f"[测试抽卡记录] 获取 {gacha_type_code} 失败: {res}")
            return None

        data = res.get("data")
        if not isinstance(data, dict) or not isinstance(data.get("list"), list):
            logger.warning(f"[测试抽卡记录] {gacha_type_code} 返回数据格式错误")
            return None
        has_more = data.get("has_more", False)
        next_max_id = data.get("next_max_id")
        version_id = data.get("version_id")
        raw_list: list[RawGachaRecord] = data.get("list", [])

        for item in raw_list:
            item_id_str = item["id"]
            if item_id_str == "0" and item["item"] is None:
                pity_count = item["gacha_count"]
                continue

            saw_records = True
            if stop_pagination:
                continue
            if not is_force and latest_id and int(item_id_str) <= int(latest_id):
                stop_pagination = True
                continue

            item_info = item["item"]
            if item_info is None:
                continue

            item_type_name = "角色" if "Avatar" in item_info["item_type"] else "光锥"
            time_str = _timestamp_to_time_str(item_id_str)

            record: SingleGachaRecord = {
                "uid": str(uid),
                "gacha_id": "",
                "gacha_type": gacha_type_id,
                "item_id": str(item_info["item_id"]),
                "count": "1",
                "time": time_str,
                "name": item_info["name"],
                "lang": "zh-cn",
                "item_type": item_type_name,
                "rank_type": str(item_info["rarity"]),
                "id": item_id_str,
                "gacha_count": item["gacha_count"],
                "is_up": item["is_up"],
            }
            records.append(record)

        if stop_pagination or not has_more:
            break
        if not next_max_id:
            logger.warning(f"[测试抽卡记录] {gacha_type_code} 分页游标缺失")
            return None
        await asyncio.sleep(0.3)

    if pity_count is None and saw_records:
        logger.warning(f"[测试抽卡记录] {gacha_type_code} 保底数据缺失")
        return None
    return records, pity_count if pity_count is not None else 0


async def save_gachalogs_new(
    uid: str,
    bot: Bot,
    ev: Event,
    is_force: bool = False,
) -> str:
    async with refresh_lock(uid):
        return await _save_gachalogs_new(uid, bot, ev, is_force)


async def _save_gachalogs_new(
    uid: str,
    bot: Bot,
    ev: Event,
    is_force: bool = False,
) -> str:
    user = await GsUser.base_select_data(user_id=ev.user_id, bot_id=ev.bot_id)
    if not user or not user.cookie:
        return f"UID{uid} 获取失败: 未登录过账号, 请先[扫码登录]!"

    device_id = user.device_id or "3c183681c7f983cb"
    auth_cookie = await mys_api.login_gacha_account(uid, user.cookie)
    if not auth_cookie:
        return f"UID{uid} 验证失败: Cookie 可能已失效, 请重新[扫码登录]!"

    path = PLAYER_PATH / str(uid)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    gachalogs_wx_path = path / "gacha_logs_wx.json"

    # 读取旧记录, 隔离保存至 gacha_logs_wx.json
    history_data: dict[str, list[SingleGachaRecord]] = {k: [] for k in POOL_MAP}
    pity_counts: dict[str, int] = {}
    pool_data_time: dict[str, str] = {}

    if gachalogs_wx_path.exists():
        try:
            async with aiofiles.open(gachalogs_wx_path, encoding="UTF-8") as f:
                content = await f.read()
                raw_json = json.loads(content)
            if not isinstance(raw_json, dict) or not isinstance(raw_json.get("data"), dict):
                raise TypeError("抽卡记录 data 必须为对象")  # noqa: TRY301
            for k in POOL_MAP:
                records = raw_json["data"].get(k, [])
                if not isinstance(records, list) or any(
                    not isinstance(record, dict) or not isinstance(record.get("id"), str)
                    for record in records
                ):
                    raise ValueError(f"{k} 历史记录格式错误")  # noqa: TRY301
                history_data[k] = records
            pity_counts = raw_json.get("pity_counts", {})
            if not isinstance(pity_counts, dict):
                raise TypeError("pity_counts 必须为对象")  # noqa: TRY301
            old_pool_times = raw_json.get("pool_data_time", {})
            if not isinstance(old_pool_times, dict):
                raise TypeError("pool_data_time 必须为对象")  # noqa: TRY301
            pool_data_time = {k: old_pool_times.get(k, raw_json.get("data_time", "")) for k in POOL_MAP}
        except (OSError, ValueError, TypeError) as e:
            logger.warning(f"[测试抽卡记录] 读取旧数据失败: {e}")
            return f"UID{uid} 更新失败: 旧抽卡记录无法读取, 请检查 gacha_logs_wx.json!"

    new_added: dict[str, int] = dict.fromkeys(POOL_MAP, 0)
    failed_pools: list[str] = []

    for pool_name, (gacha_code, gacha_id) in POOL_MAP.items():
        latest_id = history_data[pool_name][0]["id"] if history_data[pool_name] else None
        try:
            fetched = await _fetch_pool_records(
                uid=uid,
                cookie=auth_cookie,
                device_id=device_id,
                gacha_type_code=gacha_code,
                gacha_type_id=gacha_id,
                is_force=is_force,
                latest_id=latest_id,
            )
        except Exception:
            logger.exception(f"[测试抽卡记录] 获取 {pool_name} 失败")
            fetched = None
        if fetched is None:
            failed_pools.append(pool_name)
            continue
        fetched_records, pity = fetched
        pity_counts[pool_name] = pity
        pool_data_time[pool_name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        existing_ids = {r["id"] for r in history_data[pool_name]}
        fresh_records = [r for r in fetched_records if r["id"] not in existing_ids]
        new_added[pool_name] = len(fresh_records)

        combined = fresh_records + history_data[pool_name]
        combined.sort(key=lambda r: -int(r["id"]) if r["id"].isdigit() else 0)
        history_data[pool_name] = combined
        await asyncio.sleep(0.3)

    if len(failed_pools) == len(POOL_MAP):
        return f"UID{uid} [sr]抽卡记录更新失败, 已保留旧数据, 请稍后重试!"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result: GachaLogsData = {
        "uid": str(uid),
        "data_time": now_str,
        "normal_gacha_num": len(history_data["群星跃迁"]),
        "begin_gacha_num": len(history_data["始发跃迁"]),
        "char_gacha_num": len(history_data["角色跃迁"]),
        "weapon_gacha_num": len(history_data["光锥跃迁"]),
        "char_collabo_gacha_num": len(history_data["角色联动跃迁"]),
        "weapon_collabo_gacha_num": len(history_data["光锥联动跃迁"]),
        "pity_counts": pity_counts,
        "pool_data_time": pool_data_time,
        "data": history_data,
    }

    write_json_atomic(gachalogs_wx_path, result)

    total_added = sum(new_added.values())

    if failed_pools:
        return (
            f"UID{uid} [sr]抽卡记录部分更新, 新增五星记录 {total_added} 条。\n"
            f"获取失败: {'、'.join(failed_pools)}, 已保留对应旧记录和保底数据, 请稍后重试!"
        )

    if total_added == 0:
        return f"UID{uid} [sr]抽卡记录更新完毕, 无新增五星记录!"

    return (
        f"UID{uid} [sr]数据更新成功!\n"
        f"本次新增五星记录 {total_added} 条:\n"
        f"角色跃迁: {new_added['角色跃迁']} 条\n"
        f"光锥跃迁: {new_added['光锥跃迁']} 条\n"
        f"群星跃迁: {new_added['群星跃迁']} 条\n"
        f"角色联动: {new_added['角色联动跃迁']} 条\n"
        f"光锥联动: {new_added['光锥联动跃迁']} 条\n"
        f"始发跃迁: {new_added['始发跃迁']} 条\n"
    )
