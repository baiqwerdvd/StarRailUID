from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

sv_get_info = SV('sr查询信息')


@sv_get_info.on_command(('sr', 'sruid'))
async def send_role_info(bot: Bot, ev: Event):
    await bot.send("WIP 前面的区域，以后再来探索吧")
