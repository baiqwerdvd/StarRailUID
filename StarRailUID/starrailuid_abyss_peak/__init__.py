import re

from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind

from ..utils.error_reply import UID_HINT
from .draw_abyss_card import draw_abyss_img

sv_abyss_boss = SV("sr查询异相仲裁")


@sv_abyss_boss.on_command(
    (
        "查询异相仲裁",
        "查询上期异相仲裁",
        "上期仲裁",
        "异相仲裁",
        "仲裁",
        "yxzc"
    ),
    block=True,
)
async def send_srabyss_info(bot: Bot, ev: Event):
    name = "".join(re.findall("[\u4e00-\u9fa5]", ev.text))
    if name:
        return None

    logger.info("开始执行[sr查询异相仲裁信息]")
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True)
    if uid is None:
        return await bot.send(UID_HINT)
    logger.info(f"[sr查询异相仲裁信息]uid: {uid}")

    if "上期" in ev.command:
        schedule_type = "3"
    else:
        schedule_type = "1"
    logger.info(f"[sr查询异相仲裁信息]异相仲裁期数: {schedule_type}")

    im = await draw_abyss_img(ev, uid, schedule_type)
    await bot.send(im)
    return None