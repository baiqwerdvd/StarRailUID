import re

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img

from ..utils.map.name_covert import alias_to_char_name
from ..utils.resource.RESOURCE_PATH import (
    WIKI_ROLE_PATH,
    WIKI_RELIC_PATH,
    WIKI_LIGHT_CONE_PATH,
    WIKI_MATERIAL_FOR_ROLE,
)

sv_sr_wiki = SV('星铁WIKI')


@sv_sr_wiki.on_prefix(('sr角色攻略'))
async def send_role_wiki_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}攻略'.format(msg))
    name = await alias_to_char_name(msg)
    img = WIKI_ROLE_PATH / '{}.png'.format(name)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}攻略图片成功！'.format(name))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}攻略图片'.format(name))


@sv_sr_wiki.on_prefix(('sr遗器'))
async def send_relic_wiki_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}遗器'.format(msg))
    img = WIKI_RELIC_PATH / '{}.png'.format(msg)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}攻略图片成功！'.format(msg))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}攻略图片'.format(msg))


@sv_sr_wiki.on_prefix(('sr突破材料'))
async def send_material_for_role_wiki_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}突破材料'.format(msg))
    img = WIKI_MATERIAL_FOR_ROLE / '{}.png'.format(msg)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}攻略图片成功！'.format(msg))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}攻略图片'.format(msg))


@sv_sr_wiki.on_prefix(('sr武器'))
async def send_light_cone_wiki_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}武器'.format(msg))
    img = WIKI_LIGHT_CONE_PATH / '{}.png'.format(msg)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}攻略图片成功！'.format(msg))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}攻略图片'.format(msg))
