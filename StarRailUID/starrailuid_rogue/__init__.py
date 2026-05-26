import re

from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.database.models import GsBind

from .draw_rogue_card import draw_rogue_img, draw_rogue_locust_img
from .draw_rogue_tourn_card import draw_rogue_tourn_img
from ..utils.error_reply import UID_HINT

sv_srabyss = SV("sr查询模拟宇宙")
sv_srabyss_locust = SV("sr查询寰宇蝗灾")
sv_srrogue_tourn = SV("sr查询差分宇宙")


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

    logger.info("开始执行[sr查询模拟宇宙信息]")
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True, pattern=r"\d{9}")
    if uid is None:
        return await bot.send(UID_HINT)
    logger.info(f"[sr查询模拟宇宙信息]uid: {uid}")

    if "sq" in ev.command or "上期" in ev.command:
        schedule_type = "2"
    else:
        schedule_type = "3"
    logger.info(f"[sr查询模拟宇宙信息]模拟宇宙期数: {schedule_type}")

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
    logger.info(f"[sr查询模拟宇宙信息]模拟宇宙世界数: {floor}")
    im = await draw_rogue_img(ev, uid, floor, schedule_type)
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

    logger.info("开始执行[sr查询寰宇蝗灾信息]")
    uid, user_id = await get_uid(bot, ev, GsBind, "sr", True, pattern=r"\d{9}")
    if uid is None:
        return await bot.send(UID_HINT)
    logger.info(f"[sr查询寰宇蝗灾信息]uid: {uid}")
    im = await draw_rogue_locust_img(ev, uid)
    await bot.send(im)
    return None


@sv_srrogue_tourn.on_command(
    (
        "常规差分宇宙",
        "常规演算",
        "本期差分宇宙",
        "本期演算",
        "本周演算",
        "上期差分宇宙",
        "上期演算",
        "上周演算",
        "周期演算",
        "差分宇宙",
        "差分",
    ),
    block=True,
)
async def send_srrogue_tourn_info(bot: Bot, ev: Event):
    logger.info("开始执行[sr查询差分宇宙信息]")
    uid, _user_id = await get_uid(bot, ev, GsBind, "sr", True, pattern=r"\d{9}")
    if uid is None:
        return await bot.send(UID_HINT)

    if "常规" in ev.command:
        mode = "normal"
    elif "上期" in ev.command or "上周" in ev.command:
        mode = "last_week"
    elif "本期" in ev.command or "本周" in ev.command or "周期" in ev.command:
        mode = "current_week"
    else:
        mode = "overview"

    index_map = {"一": 1, "二": 2, "三": 3}
    text = ev.text.strip()
    index = int(text) if text.isdigit() else index_map.get(text, 1)
    im = await draw_rogue_tourn_img(uid, mode, index)
    await bot.send(im)
    return None
