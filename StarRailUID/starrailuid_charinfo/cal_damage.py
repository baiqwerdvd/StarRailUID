from typing import Dict

from .mono.Character import Character
from .damage.Avatar import AvatarInstance


async def cal_char_info(char_data: Dict):
    char: Character = Character(char_data)
    await char.get_equipment_info()
    await char.get_char_attribute_bonus()
    await char.get_relic_info()
    return char


async def cal_info(char_data: Dict):
    char = await cal_char_info(char_data)
    avatar = AvatarInstance(char)
    return await avatar.gat_damage()
