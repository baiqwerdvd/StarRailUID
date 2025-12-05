import re

from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.segment import MessageSegment
from gsuid_core.sv import SV

from ..utils.mys_api import mys_api

sv_get_exchange_code = SV("sr兑换码")


@sv_get_exchange_code.on_fullmatch("兑换码")
async def send_monthly_data(bot: Bot, ev: Event):
    act_id = await mys_api.get_sr_act_id()
    logger.debug(f"活动ID获取结果: {act_id}")
    if not isinstance(act_id, str):
        await bot.send("获取活动ID失败，当前可能没有直播活动")
        return
    code_ver = await mys_api.get_sr_code_ver(act_id)
    logger.debug(f"兑换码版本获取结果: {code_ver}")
    if not isinstance(code_ver, str):
        await bot.send("获取兑换码版本失败，请稍后再试")
        return
    code = await mys_api.get_sr_exchange_code(code_ver, act_id)
    logger.debug(f"兑换码获取结果: {code}")
    if str(code) == "-500012":
        await bot.send("本期直播活动已结束，请等待下一次直播")
        return
    if not isinstance(code, list):
        await bot.send("获取兑换码失败，请稍后再试")
        return
    msg = ["崩坏：星穹铁道直播兑换码"]
    for item in code:
        clean_text = re.sub(r"<[^>]+>", "", item["title"])
        clean_text = clean_text.replace("，", " ")
        msg.append(clean_text)
        msg.append(item["code"])
    await bot.send(MessageSegment.node(msg))
    return
