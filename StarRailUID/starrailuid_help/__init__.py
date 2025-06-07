from gsuid_core.bot import Bot
from gsuid_core.help.utils import register_help
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
from PIL import Image

from ..utils.error_reply import prefix
from .get_help import ICON, get_help

sv_sr_help = SV("sr帮助")


@sv_sr_help.on_fullmatch("帮助")
async def send_help_img(bot: Bot, ev: Event):
    logger.info("开始执行[sr帮助]")
    im = await get_help()
    await bot.send(im)


register_help("StarRailUID", f"{prefix}帮助", Image.open(ICON))
