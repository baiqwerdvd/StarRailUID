from .SR_MAP_PATH import EquipmentID2Name, avatarId2Name


async def avatar_id_to_name(avatar_id: str) -> str:
    char_name = avatarId2Name[avatar_id]
    return char_name


async def name_to_avatar_id(name: str) -> str:
    avatar_id = ''
    for i in avatarId2Name:
        if avatarId2Name[i] == name:
            avatar_id = i
            break
    return avatar_id


async def weapon_id_to_name(weapon_id: str) -> str:
    weapon_name = EquipmentID2Name[weapon_id]
    return weapon_name


async def name_to_weapon_id(name: str) -> str:
    weapon_id = ''
    for i in EquipmentID2Name:
        if EquipmentID2Name[i] == name:
            weapon_id = i
            break
    return weapon_id
