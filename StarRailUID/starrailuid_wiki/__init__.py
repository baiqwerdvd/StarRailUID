import re

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img

from ..utils.map.name_covert import (
    name_to_avatar_id,
    name_to_weapon_id,
    alias_to_char_name,
)
from ..utils.resource.RESOURCE_PATH import (
    WIKI_ROLE_PATH,
    WIKI_RELIC_PATH,
    GUIDE_CHARACTER_PATH,
    WIKI_LIGHT_CONE_PATH,
    GUIDE_LIGHT_CONE_PATH,
    WIKI_MATERIAL_FOR_ROLE,
)

sv_sr_wiki = SV('星铁WIKI')
sv_sr_guide = SV('星铁攻略')


@sv_sr_wiki.on_prefix(('sr角色图鉴'))
async def send_role_wiki_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}图鉴'.format(msg))
    name = await alias_to_char_name(msg)
    img = WIKI_ROLE_PATH / '{}.png'.format(name)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}图鉴图片成功！'.format(name))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}图鉴图片'.format(name))


@sv_sr_guide.on_prefix(('sr角色攻略'))
async def send_role_guide_pic(bot: Bot, ev: Event):
    char_name = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}图鉴'.format(char_name))
    if "开拓者" in str(char_name):
        char_name = "开拓者"
    char_id = await name_to_avatar_id(char_name)
    if char_id == '':
        char_name = await alias_to_char_name(char_name)
        char_id = await name_to_avatar_id(char_name)
    img = GUIDE_CHARACTER_PATH / '{}.png'.format(char_id)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}图鉴图片成功！'.format(char_id))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}图鉴图片'.format(char_id))


@sv_sr_guide.on_prefix(('sr光锥攻略'))
async def send_weapon_guide_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}图鉴'.format(msg))
    light_cone_id = await name_to_weapon_id(msg)
    img = GUIDE_LIGHT_CONE_PATH / '{}.png'.format(light_cone_id)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}光锥图片成功！'.format(light_cone_id))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}光锥图片'.format(light_cone_id))


@sv_sr_wiki.on_prefix(('sr遗器'))
async def send_relic_wiki_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}遗器'.format(msg))
    img = WIKI_RELIC_PATH / '{}.png'.format(msg)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}遗器图片成功！'.format(msg))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}遗器图片'.format(msg))


@sv_sr_wiki.on_prefix(('sr突破材料'))
async def send_material_for_role_wiki_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}突破材料'.format(msg))
    img = WIKI_MATERIAL_FOR_ROLE / '{}.png'.format(msg)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}突破材料图片成功！'.format(msg))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}突破材料图片'.format(msg))


@sv_sr_wiki.on_prefix(('sr武器'))
async def send_light_cone_wiki_pic(bot: Bot, ev: Event):
    msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', ev.text))
    await bot.logger.info('开始获取{}武器'.format(msg))
    img = WIKI_LIGHT_CONE_PATH / '{}.png'.format(msg)
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info('获得{}武器图片成功！'.format(msg))
        await bot.send(img)
    else:
        await bot.logger.warning('未找到{}武器图片'.format(msg))
