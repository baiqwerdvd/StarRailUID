import re

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from utils.convert import get_uid
from gsuid_core.models import Event

from .draw_roleinfo_card import get_role_img

sv_get_info = SV('sr查询信息')


@sv_get_info.on_command(('sruid'))
async def send_role_info(bot: Bot, ev: Event):
    name = ''.join(re.findall('[\u4e00-\u9fa5]', ev.text))
    if name:
        return

    uid = await get_uid(bot, ev)
    if uid is None:
        return '你还没有绑定UID噢,请使用[sr绑定uid123]完成绑定!'

    await bot.logger.info('开始执行[sr查询信息]')
    await bot.send(await get_role_img(uid))
