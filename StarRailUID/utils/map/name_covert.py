from .SR_MAP_PATH import (
    EquipmentID2EnName,
    EquipmentID2Name,
    SetId2Name,
    alias_data,
    avatarId2Name,
    avatarId2Rarity,
)


async def name_to_relic_set_id(name: str):
    for set_name in SetId2Name:
        if set_name == name:
            return SetId2Name[set_name]
    return None


async def avatar_id_to_name(avatar_id: str) -> str:
    return avatarId2Name[avatar_id]


async def name_to_avatar_id(name: str) -> str:
    avatar_id = ''
    for i in avatarId2Name:
        if avatarId2Name[i] == name:
            avatar_id = i
            break
    return avatar_id


async def avatar_id_to_char_star(char_id: str) -> str:
    return avatarId2Rarity[str(char_id)]


async def alias_to_char_name(char_name: str) -> str:
    for i in alias_data['characters']:
        if char_name in alias_data['characters'][i]:
            return alias_data['characters'][i][0]
    return char_name


async def alias_to_weapon_name(weapon_name: str) -> str:
    for i in alias_data['light_cones']:
        if weapon_name in alias_data['light_cones'][i]:
            return alias_data['light_cones'][i][0]
    return weapon_name


async def weapon_id_to_name(weapon_id: str) -> str:
    return EquipmentID2Name[weapon_id]


async def name_to_weapon_id(name: str) -> str:
    weapon_id = ''
    for i in EquipmentID2Name:
        if EquipmentID2Name[i] == name:
            weapon_id = i
            break
    return weapon_id


async def weapon_id_to_en_name(weapon_id: str) -> str:
    return EquipmentID2EnName[weapon_id]


async def en_name_to_weapon_id(name: str) -> str:
    weapon_id = ''
    for i in EquipmentID2EnName:
        if EquipmentID2EnName[i] == name:
            weapon_id = i
            break
    return weapon_id
