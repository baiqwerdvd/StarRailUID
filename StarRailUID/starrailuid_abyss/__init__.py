import re

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.logger import logger
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind

from ..utils.error_reply import UID_HINT
from .draw_abyss_card import draw_abyss_img

sv_srabyss = SV("sr查询深渊")


@sv_srabyss.on_command(
    (
        "查询深渊",
        "查询上期深渊",
        "上期深渊",
        "深渊",
    ),
    block=True,
)
async def send_srabyss_info(bot: Bot, ev: Event):
    name = "".join(re.findall("[\u4e00-\u9fa5]", ev.text))
    if name:
        return None

    logger.info("开始执行[sr查询深渊信息]")
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True)
    if uid is None:
        return await bot.send(UID_HINT)
    logger.info(f"[sr查询深渊信息]uid: {uid}")

    if "上期" in ev.command:
        schedule_type = "2"
    else:
        schedule_type = "1"
    logger.info(f"[sr查询深渊信息]深渊期数: {schedule_type}")

    im = await draw_abyss_img(ev, uid, schedule_type)
    await bot.send(im)
    return None
