from typing import Union

from gsuid_core.aps import scheduler
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.subscribe import gs_subscribe
from gsuid_core.sv import SV
from gsuid_core.utils.database.models import GsBind
from gsuid_core.utils.sign.sign import sign_in

from ..starrailuid_config.sr_config import srconfig
from ..utils.error_reply import UID_HINT

SIGN_TIME = srconfig.get_config("SignTime").data
IS_REPORT = srconfig.get_config("PrivateSignReport").data

sv_sign = SV("星穹铁道签到")
sv_sign_config = SV("星穹铁道管理", pm=2)


@sv_sign.on_fullmatch("签到")
async def get_sign_func(bot: Bot, ev: Event):
    logger.info(f"[星穹铁道] [签到] 用户: {ev.user_id}")
    uid = await GsBind.get_uid_by_game(ev.user_id, ev.bot_id, "sr")
    if uid is None:
        return await bot.send(UID_HINT)
    logger.info(f"[星穹铁道] [签到] UID: {uid}")
    await bot.send(await sign_in(uid, "sr"))
    return None


@sv_sign_config.on_fullmatch('全部重签')
async def recheck(bot: Bot, ev: Event):
    logger.info('开始执行[全部重签]')
    await bot.send('🚩 [星铁] [全部重签] 已开始执行...')
    await send_daily_sign(True)
    await bot.send('🚩 [星铁] [全部重签] 执行完成！')


async def sign_in_task(uid: Union[str, int]):
    return await sign_in(str(uid), 'sr')

# 每日零点半执行米游社星穹铁道签到
@scheduler.scheduled_job("cron", hour=SIGN_TIME[0], minute=SIGN_TIME[1])
async def sr_sign_at_night():
    await send_daily_sign()



async def send_daily_sign(force: bool = False):
    logger.info('[星铁] 开始执行[每日全部签到]')
    if srconfig.get_config("SchedSignin").data or force:
        # 执行签到 并获得推送消息
        datas = await gs_subscribe.get_subscribe('[星铁] 自动签到')
        priv_result, group_result = await gs_subscribe.muti_task(
            datas, sign_in_task, 'uid'
        )

        if not IS_REPORT:
            priv_result = {}

        for _, data in priv_result.items():
            im = '\n'.join(data['im'])
            event = data['event']
            await event.send(im)

        for _, data in group_result.items():
            im = '✅ 星铁今日自动签到已完成！\n'
            im += f'📝 本群共签到成功{data["success"]}人，共签到失败{data["fail"]}人。'
            event = data['event']
            await event.send(im)

        logger.info('[星铁] [每日全部签到] 推送完成')
    else:
        logger.info('[星铁] 未开启[每日全部签到]')