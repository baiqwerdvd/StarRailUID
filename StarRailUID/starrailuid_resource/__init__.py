from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.logger import logger

from ..utils.resource.download_all_file import check_use

sv_sr_download_config = SV("sr下载资源", pm=1)


@sv_sr_download_config.on_fullmatch("下载全部资源")
async def send_download_resource_msg(bot: Bot, ev: Event):
    await bot.send("sr正在开始下载~可能需要较久的时间!")
    im = await check_use()
    await bot.send(im)


async def startup():
    logger.info("[sr资源文件下载] 正在检查与下载缺失的资源文件,可能需要较长时间,请稍等")
    logger.info(f"[sr资源文件下载] {await check_use()}")
