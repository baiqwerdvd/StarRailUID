import re

from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.image.convert import convert_img

from ..utils.map.name_covert import (
    alias_to_char_name,
    name_to_avatar_id,
    name_to_relic_set_id,
    name_to_weapon_id,
)
from ..utils.resource.RESOURCE_PATH import (
    GUIDE_CHARACTER_PATH,
    GUIDE_LIGHT_CONE_PATH,
    WIKI_LIGHT_CONE_PATH,
    WIKI_MATERIAL_FOR_ROLE,
    WIKI_RELIC_PATH,
    WIKI_ROLE_PATH,
)

sv_sr_wiki = SV("星铁WIKI")
sv_sr_guide = SV("星铁攻略")


@sv_sr_wiki.on_prefix("sr角色图鉴")
async def send_role_wiki_pic(bot: Bot, ev: Event):
    char_name = " ".join(re.findall("[\u4e00-\u9fa5]+", ev.text))
    await bot.logger.info(f"开始获取{char_name}图鉴")
    if "开拓者" in str(char_name):
        char_name = "开拓者"
    char_id = await name_to_avatar_id(char_name)
    if char_id == "":
        char_name = await alias_to_char_name(char_name)
        char_id = await name_to_avatar_id(char_name)
    img = WIKI_ROLE_PATH / f"{char_id}.png"
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info(f"获得{char_name}图鉴图片成功!")
        await bot.send(img)
    else:
        await bot.logger.warning(f"未找到{char_name}图鉴图片")


@sv_sr_guide.on_prefix("sr角色攻略")
async def send_role_guide_pic(bot: Bot, ev: Event):
    char_name = " ".join(re.findall("[\u4e00-\u9fa5]+", ev.text))
    await bot.logger.info(f"开始获取{char_name}图鉴")
    if "开拓者" in str(char_name):
        char_name = "开拓者"
    char_id = await name_to_avatar_id(char_name)
    if char_id == "":
        char_name = await alias_to_char_name(char_name)
        char_id = await name_to_avatar_id(char_name)
    img = GUIDE_CHARACTER_PATH / f"{char_id}.png"
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info(f"获得{char_id}图鉴图片成功!")
        await bot.send(img)
    else:
        await bot.logger.warning(f"未找到{char_id}图鉴图片")


@sv_sr_guide.on_prefix("sr光锥攻略")
async def send_weapon_guide_pic(bot: Bot, ev: Event):
    msg = " ".join(re.findall("[\u4e00-\u9fa5]+", ev.text))
    await bot.logger.info(f"开始获取{msg}图鉴")
    light_cone_id = await name_to_weapon_id(msg)
    img = GUIDE_LIGHT_CONE_PATH / f"{light_cone_id}.png"
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info(f"获得{light_cone_id}光锥图片成功!")
        await bot.send(img)
    else:
        await bot.logger.warning(f"未找到{light_cone_id}光锥图片")


@sv_sr_wiki.on_prefix("sr遗器")
async def send_relic_wiki_pic(bot: Bot, ev: Event):
    msg = " ".join(re.findall("[\u4e00-\u9fa5]+", ev.text))
    await bot.logger.info(f"开始获取{msg}遗器")
    set_id = await name_to_relic_set_id(msg)
    img = WIKI_RELIC_PATH / f"{set_id}.png"
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info(f"获得{msg}遗器图片成功!")
        await bot.send(img)
    else:
        await bot.logger.warning(f"未找到{msg}遗器图片")


@sv_sr_wiki.on_prefix("sr突破材料")
async def send_material_for_role_wiki_pic(bot: Bot, ev: Event):
    char_name = " ".join(re.findall("[\u4e00-\u9fa5]+", ev.text))
    await bot.logger.info(f"开始获取{char_name}突破材料")
    if "开拓者" in str(char_name):
        char_name = "开拓者"
    char_id = await name_to_avatar_id(char_name)
    if char_id == "":
        char_name = await alias_to_char_name(char_name)
        char_id = await name_to_avatar_id(char_name)
    img = WIKI_MATERIAL_FOR_ROLE / f"{char_id}.png"
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info(f"获得{char_name}突破材料图片成功!")
        await bot.send(img)
    else:
        await bot.logger.warning(f"未找到{char_name}突破材料图片")


@sv_sr_wiki.on_prefix("sr武器")
async def send_light_cone_wiki_pic(bot: Bot, ev: Event):
    msg = " ".join(re.findall("[\u4e00-\u9fa5]+", ev.text))
    await bot.logger.info(f"开始获取{msg}武器")
    light_cone_id = await name_to_weapon_id(msg)
    img = WIKI_LIGHT_CONE_PATH / f"{light_cone_id}.png"
    if img.exists():
        img = await convert_img(img)
        await bot.logger.info(f"获得{msg}武器图片成功!")
        await bot.send(img)
    else:
        await bot.logger.warning(f"未找到{msg}武器图片")
