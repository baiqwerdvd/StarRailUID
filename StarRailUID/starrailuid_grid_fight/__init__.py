import re

from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind

from ..utils.error_reply import UID_HINT
from .draw_grid_card import draw_grid_img

sv_grid_fight = SV("sr查询货币战争")


@sv_grid_fight.on_command(
    ("查询货币战争", "货币战争", "战争", "hbzz"),
    block=True,
)
async def send_srabyss_info(bot: Bot, ev: Event):
    name = "".join(re.findall("[\u4e00-\u9fa5]", ev.text))
    if name:
        return None

    logger.info("开始执行[sr查询货币战争信息]")
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True)
    if uid is None:
        return await bot.send(UID_HINT)
    logger.info(f"[sr查询货币战争信息]uid: {uid}")

    im = await draw_grid_img(ev, uid)
    await bot.send(im)
    return None
