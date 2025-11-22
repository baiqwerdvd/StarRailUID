from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
from starrail_damage_cal.update import update_resource

from ..utils.excel.read_excel import update_light_cone_ranks
from ..utils.resource.download_all_file import check_use

sv_sr_download_config = SV("sr下载资源", pm=1)


@sv_sr_download_config.on_fullmatch("下载全部资源")
async def send_download_resource_msg(bot: Bot, ev: Event):
    await bot.send("sr正在开始下载~可能需要较久的时间!")
    im = await check_use()
    await bot.send(im)
    await bot.send("尝试更新数据文件")
    im = await update_resource()
    await bot.send(im)
    await bot.send("尝试更新光追评价")
    im = await update_light_cone_ranks()
    await bot.send(im)
    try:
        import importlib

        import starrail_damage_cal.excel.model
        import starrail_damage_cal.map.SR_MAP_PATH

        importlib.reload(starrail_damage_cal.map.SR_MAP_PATH)
        importlib.reload(starrail_damage_cal.excel.model)

        await bot.send("✅ 数据模块已重新加载")
    except Exception:
        logger.exception("重载数据时出错")
        await bot.send("⚠️ 重载数据可能发生异常，建议重新启动以重载数据")


async def startup():
    logger.info("[sr资源文件下载] 正在检查与下载缺失的资源文件,可能需要较长时间,请稍等")
    logger.info(f"[sr资源文件下载] {await check_use()}")
