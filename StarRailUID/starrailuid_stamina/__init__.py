import asyncio

from gsuid_core.aps import scheduler
from gsuid_core.bot import Bot
from gsuid_core.gss import gss
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.segment import MessageSegment
from gsuid_core.sv import SV
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind

from .draw_stamina_card import get_stamina_img
from .notice import get_notice_list
from .stamina_text import get_stamina_text
from ..starrailuid_config.sr_config import srconfig
from ..utils.error_reply import UID_HINT

sv_get_stamina = SV("sr查询体力")
sv_get_stamina_admin = SV("sr强制推送", pm=1)


@sv_get_stamina.on_fullmatch("当前状态")
async def send_daily_info(bot: Bot, ev: Event):
    logger.info("开始执行[sr每日信息文字版]")
    uid = await get_uid(bot, ev, GsBind, "sr")
    if uid is None:
        return await bot.send(UID_HINT)
    logger.info(f"[sr每日信息文字版]UID: {uid}")

    im = await get_stamina_text(uid)
    await bot.send(im)
    return None


@sv_get_stamina_admin.on_fullmatch("强制推送体力提醒")
async def force_notice_job(bot: Bot, ev: Event):
    logger.info("开始执行[sr强制推送体力信息]")
    await sr_notice_job()


@scheduler.scheduled_job("cron", minute="*/30")
async def sr_notice_job():
    StaminaCheck = srconfig.get_config("StaminaCheck").data
    if not StaminaCheck:
        logger.trace("[sr推送检查] 暂停...")
        return

    result = await get_notice_list()
    logger.info("[sr推送检查]完成!等待消息推送中...")
    logger.debug(result)

    # 执行私聊推送
    for bot_id in result:
        for BOT_ID in gss.active_bot:
            bot = gss.active_bot[BOT_ID]
            for user_id in result[bot_id]["direct"]:
                msg = result[bot_id]["direct"][user_id]
                await bot.target_send(msg, "direct", user_id, bot_id, "", "")
                await asyncio.sleep(0.5)
            logger.info("[sr推送检查] 私聊推送完成")
            for gid in result[bot_id]["group"]:
                msg_list = []
                for user_id in result[bot_id]["group"][gid]:
                    msg_list.append(MessageSegment.at(user_id))
                    msg = result[bot_id]["group"][gid][user_id]
                    msg_list.append(MessageSegment.text(msg))
                await bot.target_send(msg_list, "group", gid, bot_id, "", "")
                await asyncio.sleep(0.5)
            logger.info("[sr推送检查] 群聊推送完成")


@sv_get_stamina.on_fullmatch(
    (
        "每日",
        "mr",
        "实时便笺",
        "便笺",
        "便签",
    )
)
async def send_daily_info_pic(bot: Bot, ev: Event):
    logger.info("开始执行[sr每日信息]")
    user_id = ev.at if ev.at else ev.user_id
    logger.info(f"[sr每日信息]QQ号: {user_id}")

    im = await get_stamina_img(bot.bot_id, user_id)
    await bot.send(im)
