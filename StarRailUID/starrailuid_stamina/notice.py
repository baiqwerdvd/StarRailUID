from typing import Dict

from gsuid_core.gss import gss
from gsuid_core.logger import logger

from ..sruid_utils.api.mys.models import DailyNoteData
from ..starrailuid_config.sr_config import srconfig
from ..utils.api import get_sqla
from ..utils.mys_api import mys_api

MR_NOTICE = '\n可发送[srmr]或者[sr每日]来查看更多信息!\n'

NOTICE = {
    'stamina': f'你的开拓力快满啦!{MR_NOTICE}',
    'go': f'你有派遣信息即将可收取!{MR_NOTICE}',
}


async def get_notice_list() -> Dict[str, Dict[str, Dict]]:
    msg_dict: Dict[str, Dict[str, Dict]] = {}
    for bot_id in gss.active_bot:
        sqla = get_sqla(bot_id)
        user_list = await sqla.get_all_push_user_list()
        for user in user_list:
            if user.sr_uid is not None:
                raw_data = await mys_api.get_daily_data(user.sr_uid)
                if isinstance(raw_data, int):
                    logger.error(f'[sr推送提醒]获取{user.sr_uid}的数据失败!')
                    continue
                push_data = await sqla.select_push_data(user.sr_uid)
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
    sqla = get_sqla(bot_id)
    for mode in NOTICE.keys():
        # 检查条件
        if push_data[f'{mode}_is_push'] == 'on':
            if srconfig.get_config('CrazyNotice').data:
                if not await check(mode, raw_data, push_data[f'{mode}_value']):
                    await sqla.update_push_data(
                        uid, {f'{mode}_is_push': 'off'}
                    )
                continue
        # 准备推送
        if await check(mode, raw_data, push_data[f'{mode}_value']):
            if push_data[f'{mode}_push'] == 'off':
                pass
            # on 推送到私聊
            else:
                # 初始化
                if bot_id not in msg_dict:
                    msg_dict[bot_id] = {'direct': {}, 'group': {}}

                if push_data[f'{mode}_push'] == 'on':
                    # 添加私聊信息
                    if user_id not in msg_dict[bot_id]['direct']:
                        msg_dict[bot_id]['direct'][user_id] = NOTICE[mode]
                    else:
                        msg_dict[bot_id]['direct'][user_id] += NOTICE[mode]
                    await sqla.update_push_data(uid, {f'{mode}_is_push': 'on'})
                # 群号推送到群聊
                else:
                    # 初始化
                    gid = push_data[f'{mode}_push']
                    if gid not in msg_dict[bot_id]['group']:
                        msg_dict[bot_id]['group'][gid] = {}

                    if user_id not in msg_dict[bot_id]['group'][gid]:
                        msg_dict[bot_id]['group'][gid][user_id] = NOTICE[mode]
                    else:
                        msg_dict[bot_id]['group'][gid][user_id] += NOTICE[mode]
                    await sqla.update_push_data(uid, {f'{mode}_is_push': 'on'})
    return msg_dict


async def check(mode: str, data: DailyNoteData, limit: int) -> bool:
    if mode == 'resin':
        if data['current_stamina'] >= limit:
            return True
        if data['current_stamina'] >= data['max_stamina']:
            return True
        return False
    if mode == 'go':
        for i in data['expeditions']:
            if i['status'] == 'Ongoing':
                if int(i['remaining_time']) <= limit * 60:
                    return True
            else:
                return True
        return False
    return False
