import re

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind

from ..utils.error_reply import UID_HINT
from .draw_rogue_card import draw_rogue_img, draw_rogue_locust_img

sv_srabyss = SV("sr查询模拟宇宙")
sv_srabyss_locust = SV("sr查询寰宇蝗灾")


@sv_srabyss.on_command(
    (
        "查询宇宙",
        "yz",
        "查询上期宇宙",
        "sqyz",
        "上期宇宙",
        "宇宙",
        "查询模拟宇宙",
        "上期模拟宇宙",
        "查询上期模拟宇宙",
    ),
    block=True,
)
async def send_srabyss_info(bot: Bot, ev: Event):
    name = "".join(re.findall("[\u4e00-\u9fa5]", ev.text))
    if name:
        return None

    await bot.logger.info("开始执行[sr查询模拟宇宙信息]")
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True)
    if uid is None:
        return await bot.send(UID_HINT)
    await bot.logger.info(f"[sr查询模拟宇宙信息]uid: {uid}")

    if "sq" in ev.command or "上期" in ev.command:
        schedule_type = "2"
    else:
        schedule_type = "3"
    await bot.logger.info(f"[sr查询模拟宇宙信息]模拟宇宙期数: {schedule_type}")

    if ev.text in ["一", "二", "三", "四", "五", "六"]:
        floor = (
            ev.text.replace("一", "1")
            .replace("二", "2")
            .replace("三", "3")
            .replace("四", "4")
            .replace("五", "5")
            .replace("六", "6")
        )
    else:
        floor = ev.text
    if floor and floor.isdigit():
        floor = int(floor)
    else:
        floor = None
    await bot.logger.info(f"[sr查询模拟宇宙信息]模拟宇宙世界数: {floor}")
    im = await draw_rogue_img(user_id, uid, ev.sender, floor, schedule_type)
    await bot.send(im)
    return None


@sv_srabyss_locust.on_command(
    (
        "寰宇蝗灾",
        "hyhz",
        "查询寰宇蝗灾",
        "sqhyhz",
    ),
    block=True,
)
async def send_srabyss_locust_info(bot: Bot, ev: Event):
    name = "".join(re.findall("[\u4e00-\u9fa5]", ev.text))
    if name:
        return None

    await bot.logger.info("开始执行[sr查询寰宇蝗灾信息]")
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True)
    if uid is None:
        return await bot.send(UID_HINT)
    await bot.logger.info(f"[sr查询寰宇蝗灾信息]uid: {uid}")
    im = await draw_rogue_locust_img(user_id, uid, ev.sender)
    await bot.send(im)
    return None
