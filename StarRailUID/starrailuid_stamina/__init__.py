from gsuid_core.aps import scheduler
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind

from ..starrailuid_config.sr_config import srconfig
from ..utils.error_reply import UID_HINT
from .draw_stamina_card import get_stamina_img
from .notice import get_notice_list
from .stamina_text import get_stamina_text

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


@sv_get_stamina_admin.on_fullmatch("强制推送体力提醒")
async def force_notice_job(bot: Bot, ev: Event):
    await bot.send("🔨 [原神服务]\n🌱 开始执行强制推送体力提醒!")
    await sr_notice_job(True)
    await bot.send("🔨 [原神服务]\n✅ 强制推送体力提醒执行完成!")


@scheduler.scheduled_job("cron", minute="*/30")
async def sr_notice_job(force: bool = False):
    StaminaCheck = srconfig.get_config("StaminaCheck").data
    if StaminaCheck or force:
        await get_notice_list()
        logger.info("[星铁服务] [推送检查] 完成!")
    else:
        logger.info("🔨 [原神服务]\n❌ 未开启推送检查功能!")


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
