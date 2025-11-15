from typing import Optional

from starrail_damage_cal.excel import model
from starrail_damage_cal.map import SR_MAP_PATH


async def name_to_relic_set_id(name: str):
    for set_name in SR_MAP_PATH.SetId2Name:
        if set_name == name:
            return SR_MAP_PATH.SetId2Name[set_name]
    return None


async def name_to_avatar_id(name: str) -> str:
    avatar_id = ""
    for i in SR_MAP_PATH.avatarId2Name:
        if SR_MAP_PATH.avatarId2Name[i] == name:
            avatar_id = i
            break
    return avatar_id


async def avatar_id_to_char_star(char_id: str) -> str:
    return SR_MAP_PATH.avatarId2Rarity[str(char_id)]


async def alias_to_char_id(char_name: str) -> Optional[str]:
    for i in model.CharAlias["characters"]:
        for j in model.CharAlias["characters"][i]:
            if char_name in j:
                return i
    return None


async def alias_to_char_name(char_name: str) -> str:
    for i in model.CharAlias["characters"]:
        if char_name in model.CharAlias["characters"][i]:
            return model.CharAlias["characters"][i][0]
    return char_name


async def alias_to_weapon_name(weapon_name: str) -> str:
    for i in model.CharAlias["light_cones"]:
        if weapon_name in model.CharAlias["light_cones"][i]:
            return model.CharAlias["light_cones"][i][0]
    return weapon_name


async def name_to_weapon_id(name: str) -> str:
    weapon_id = ""
    for i in SR_MAP_PATH.EquipmentID2Name:
        if SR_MAP_PATH.EquipmentID2Name[i] == name:
            weapon_id = i
            break
    return weapon_id
