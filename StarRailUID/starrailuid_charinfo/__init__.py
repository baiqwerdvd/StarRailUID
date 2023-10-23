import re
from pathlib import Path
from typing import Tuple, cast
import asyncio
from PIL import Image
from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .cal_damage import cal_info
from .to_card import api_to_card
from ..utils.convert import get_uid
from ..utils.sr_prefix import PREFIX
from ..utils.error_reply import UID_HINT
from .draw_char_img import get_char_data
from .get_char_img import draw_char_info_img
from ..utils.image.convert import convert_img
from ..utils.resource.RESOURCE_PATH import TEMP_PATH

sv_char_info_config = SV('sr面板设置', pm=2)
sv_get_char_info = SV('sr面板查询', priority=10)
sv_get_sr_original_pic = SV('sr查看面板原图', priority=5)

@sv_get_char_info.on_prefix(f'{PREFIX}查询')
async def send_char_info(bot: Bot, ev: Event):
    im = await _get_char_info(bot, ev, ev.text)
    if isinstance(im, str):
        await bot.send(im)
    elif isinstance(im, Tuple):
        if isinstance(im[0], Image.Image):
            img = await convert_img(cast(Image.Image, im[0]))
        else:
            img = str(im[0])
        await bot.send(img)
        if im[1]:
            with Path.open(TEMP_PATH / f'{ev.msg_id}.jpg', 'wb') as f:
                f.write(cast(bytes, im[1]))
    elif isinstance(im, Image.Image):
        await bot.send(await convert_img(im))
    elif isinstance(im, bytes):
        await bot.send(im)
    elif im is None:
        return
    else:
        await bot.send('发生未知错误')


async def _get_char_info(bot: Bot, ev: Event, text: str):
    # msg = ''.join(re.findall('^[a-zA-Z0-9_\u4e00-\u9fa5]+$', text))
    msg = text
    if not msg:
        return None
    # 获取角色名
    await bot.logger.info('开始执行[查询角色面板]')
    # 获取uid
    if '换' in msg or '拿' in msg or '带' in msg:
        uid = await get_uid(bot, ev, False, True)
    else:
        uid = await get_uid(bot, ev)
        msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', text))
    if uid is None:
        return await bot.send(UID_HINT)
    await bot.logger.info(f'[查询角色面板]uid: {uid}')

    return await draw_char_info_img(msg, uid)


@sv_get_char_info.on_command(f'{PREFIX}强制刷新')
async def send_card_info(bot: Bot, ev: Event):
    uid = await get_uid(bot, ev)
    if uid is None:
        return await bot.send(UID_HINT)
    await bot.logger.info(f'[sr强制刷新]uid: {uid}')
    im = await api_to_card(uid)
    await bot.logger.info(f'UID{uid}获取角色数据成功!')
    await bot.send(im)
    return None
