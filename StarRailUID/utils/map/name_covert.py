from .SR_MAP_PATH import (
    EquipmentID2Name,
    EquipmentID2EnName,
    alias_data,
    avatarId2Name,
    avatarId2Rarity,
)


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
