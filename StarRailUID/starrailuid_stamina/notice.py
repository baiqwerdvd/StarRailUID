from typing import Dict

from gsuid_core.gss import gss
from gsuid_core.logger import logger
from gsuid_core.utils.database.models import GsUser

from ..sruid_utils.api.mys.models import DailyNoteData
from ..starrailuid_config.sr_config import srconfig
from ..utils.database.model import SrPush
from ..utils.mys_api import mys_api

MR_NOTICE = "\n可发送[srmr]或者[sr每日]来查看更多信息!\n"

NOTICE = {
    "stamina": f"你的开拓力已达提醒阈值!{MR_NOTICE}",
    "go": f"你的派遣已全部完成!{MR_NOTICE}",
}


async def get_notice_list() -> Dict[str, Dict[str, Dict]]:
    msg_dict: Dict[str, Dict[str, Dict]] = {}
    for _ in gss.active_bot:
        user_list = await GsUser.get_push_user_list('sr')
        for user in user_list:
            if user.sr_uid is not None:
                raw_data = await mys_api.get_sr_daily_data(user.sr_uid)
                if isinstance(raw_data, int):
                    logger.error(f"[sr推送提醒]获取{user.sr_uid}的数据失败!")
                    continue
                push_data = await SrPush.select_data_by_uid(user.sr_uid, "sr")
                msg_dict = await all_check(
                    user.bot_id,
                    raw_data,
                    push_data.__dict__,
                    msg_dict,
                    user.user_id,
                    user.sr_uid,
                )
    return msg_dict


async def all_check(
    bot_id: str,
    raw_data: DailyNoteData,
    push_data: Dict,
    msg_dict: Dict[str, Dict[str, Dict]],
    user_id: str,
    uid: str,
) -> Dict[str, Dict[str, Dict]]:
    for mode in NOTICE.keys():
        _check = await check(
            mode,
            raw_data,
            push_data.get(f"{mode}_value", 0),
        )

        # 检查条件
        if push_data[f"{mode}_is_push"] == "on":
            if not srconfig.get_config("CrazyNotice").data:
                if not _check:
                    await SrPush.update_data_by_uid(
                        uid, bot_id, "sr", **{f"{mode}_is_push": "off"}
                    )
            continue

        # 准备推送
        if _check:
            if push_data[f"{mode}_push"] == "off":
                pass
            else:
                notice = NOTICE[mode]
                if isinstance(_check, int):
                    notice += f"(当前值: {_check})"

                direct_data = None
                group_data = None

                # 初始化
                if bot_id not in msg_dict:
                    msg_dict[bot_id] = {"direct": {}, "group": {}}
                    direct_data = msg_dict[bot_id]["direct"]
                    group_data = msg_dict[bot_id]["group"]

                if direct_data is None or group_data is None:
                    logger.error("[sr推送提醒]初始化失败!")
                    continue

                # on 推送到私聊
                if push_data[f"{mode}_push"] == "on":
                    # 添加私聊信息
                    if user_id not in direct_data:
                        direct_data[user_id] = notice
                    else:
                        direct_data[user_id] += notice
                # 群号推送到群聊
                else:
                    # 初始化
                    gid = push_data[f"{mode}_push"]
                    if gid not in group_data:
                        group_data[gid] = {}

                    if user_id not in group_data[gid]:
                        group_data[gid][user_id] = notice
                    else:
                        group_data[gid][user_id] += notice

                await SrPush.update_data_by_uid(
                    uid, bot_id, "sr", **{f"{mode}_is_push": "on"}
                )
    return msg_dict


async def check(mode: str, data: DailyNoteData, limit: int) -> bool:
    if mode == "stamina":
        if data.current_stamina >= limit:
            return True
        if data.current_stamina >= data.max_stamina:
            return True
        return False
    if mode == "go":
        count = 0
        for i in data.expeditions:
            if i.status == "Ongoing":
                count += 1
        return count == 0
    return False
