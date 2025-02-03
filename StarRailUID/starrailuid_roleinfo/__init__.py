import re

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.logger import logger
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind

from ..utils.error_reply import UID_HINT
from .draw_roleinfo_card import get_role_img, get_detail_img

sv_get_info = SV("sr查询信息")


@sv_get_info.on_command(("uid", "查询"))
async def send_role_info(bot: Bot, ev: Event):
    name = "".join(re.findall("[\u4e00-\u9fa5]", ev.text))
    if name:
        return None

    uid = await get_uid(bot, ev, GsBind, "sr")
    if uid is None:
        return await bot.send(UID_HINT)

    logger.info(f"[sr查询信息]UID: {uid}")
    logger.info("开始执行[sr查询信息]")
    await bot.send(await get_role_img(ev, uid))
    return None


@sv_get_info.on_command(("练度统计", "角色列表"))
async def send_detail_info(bot: Bot, ev: Event):
    name = "".join(re.findall("[\u4e00-\u9fa5]", ev.text))
    if name:
        return None
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True)
    if uid is None:
        return await bot.send(UID_HINT)

    logger.info(f"[sr查询信息]UID: {uid}")
    logger.info("开始执行[sr查询信息]")
    await bot.send(await get_detail_img(ev, uid))
    return None
