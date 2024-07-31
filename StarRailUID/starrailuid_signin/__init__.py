from ..starrailuid_config.sr_config import srconfig
from ..utils.error_reply import UID_HINT
from ..utils.sr_prefix import PREFIX

from gsuid_core.aps import scheduler
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.boardcast.send_msg import send_board_cast_msg
from gsuid_core.utils.database.models import GsBind
from gsuid_core.utils.sign.sign import daily_sign, sign_in

SIGN_TIME = srconfig.get_config('SignTime').data
IS_REPORT = srconfig.get_config('PrivateSignReport').data

sv_sign = SV('星穹铁道签到')
sv_sign_config = SV('星穹铁道管理', pm=2)


@sv_sign.on_fullmatch(f'{PREFIX}签到')
async def get_sign_func(bot: Bot, ev: Event):
    logger.info(f'[星穹铁道] [签到] 用户: {ev.user_id}')
    uid = await GsBind.get_uid_by_game(ev.user_id, ev.bot_id, 'sr')
    if uid is None:
        return await bot.send(UID_HINT)
    logger.info(f'[星穹铁道] [签到] UID: {uid}')
    await bot.send(await sign_in(uid, 'sr'))
    return None


@sv_sign_config.on_fullmatch(f'{PREFIX}全部重签')
async def recheck(bot: Bot, ev: Event):
    await bot.logger.info('开始执行[全部重签]')
    await bot.send('[星穹铁道] [全部重签] 已开始执行!')
    result = await daily_sign('sr')
    if not IS_REPORT:
        result['private_msg_dict'] = {}
    await send_board_cast_msg(result)
    await bot.send('[星穹铁道] [全部重签] 执行完成!')


# 每日零点半执行米游社星穹铁道签到
@scheduler.scheduled_job('cron', hour=SIGN_TIME[0], minute=SIGN_TIME[1])
async def sr_sign_at_night():
    if srconfig.get_config('SchedSignin').data:
        result = await daily_sign('sr')
        if not IS_REPORT:
            result['private_msg_dict'] = {}
        await send_board_cast_msg(result)
