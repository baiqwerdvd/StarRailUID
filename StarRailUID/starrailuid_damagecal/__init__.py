import re

from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.sv import SV

from ..starrailuid_charinfo.draw_char_img import get_char_data
from ..utils.convert import get_uid
from ..utils.error_reply import UID_HINT
from ..utils.sr_prefix import PREFIX
from .cal_damage import cal

sv_char_damage_cal = SV('sr伤害计算')


@sv_char_damage_cal.on_prefix(f'{PREFIX}伤害计算')
async def send_damage_msg(bot: Bot, ev: Event):
    msg = ''.join(re.findall('[\u4e00-\u9fa5 ]', ev.text))
    if not msg:
        return None
    await bot.logger.info('开始执行[角色伤害计算]')
    # 获取uid
    sr_uid = await get_uid(bot, ev)
    if sr_uid is None:
        return await bot.send(UID_HINT)
    await bot.logger.info(f'[角色伤害计算]uid: {sr_uid}')
    char_name = ' '.join(re.findall('[\u4e00-\u9fa5]+', msg))

    char_data = await get_char_data(sr_uid, char_name)
    if isinstance(char_data, str):
        return await bot.send(char_data)

    im = await cal(char_data)
    await bot.send(im)
    return None
