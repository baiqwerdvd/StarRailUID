import re

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .cal_damage import cal
from ..utils.convert import get_uid
from ..utils.sr_prefix import PREFIX
from ..utils.error_reply import UID_HINT
from ..starrailuid_charinfo.draw_char_img import get_char_data

sv_char_damage_cal = SV('sr伤害计算')


@sv_char_damage_cal.on_prefix(f'{PREFIX}伤害计算')
async def send_damage_msg(bot: Bot, ev: Event):
    msg = ''.join(re.findall('[\u4e00-\u9fa5 ]', ev.text))
    if not msg:
        return
    await bot.logger.info('开始执行[角色伤害计算]')
    # 获取uid
    sr_uid = await get_uid(bot, ev)
    if sr_uid is None:
        return await bot.send(UID_HINT)
    await bot.logger.info('[角色伤害计算]uid: {}'.format(sr_uid))
    char_name = ' '.join(re.findall('[\u4e00-\u9fa5]+', msg))

    char_data = await get_char_data(sr_uid, char_name)

    im = await cal(char_data)
    await bot.send(im)
