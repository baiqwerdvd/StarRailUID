import json
from pathlib import Path
import re
from typing import Dict, Optional, Tuple, Union

from gsuid_core.logger import logger
from starrail_damage_cal.excel.model import (
    AvatarPromotionConfig,
    EquipmentPromotionConfig,
)
from starrail_damage_cal.to_data import api_to_dict

from .draw_char_img import draw_char_img
from ..sruid_utils.api.mihomo.models import Character
from ..utils.error_reply import CHAR_HINT
from ..utils.map.SR_MAP_PATH import (
    AvatarRankSkillUp,
    EquipmentID2Name,
    EquipmentID2Rarity,
    Property2Name,
    avatarId2DamageType,
    avatarId2EnName,
    avatarId2Name,
    avatarId2Rarity,
    characterSkillTree,
    rankId2Name,
    skillId2AttackType,
    skillId2Effect,
    skillId2Name,
)
from ..utils.map.name_covert import (
    alias_to_char_name,
    alias_to_weapon_name,
    name_to_avatar_id,
    name_to_weapon_id,
)
from ..utils.resource.RESOURCE_PATH import PLAYER_PATH

WEAPON_TO_INT = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "满": 5,
}

CHAR_TO_INT = {
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "满": 6,
}

PieceName_ilst = {
    0: ["头", "帽"],
    1: ["手"],
    2: ["衣", "服", "躯"],
    3: ["鞋", "腿"],
    4: ["球"],
    5: ["绳", "链"],
}


async def draw_char_info_img(msg: str, uid: str):
    char = await get_char_data(uid, msg)
    char_data = Character(**char)
    if isinstance(char, str):
        logger.info("[sr查询角色] 绘图失败, 替换的武器不正确!")
        return char

    im = await draw_char_img(char_data, uid, msg)
    logger.info("[查询角色] 绘图完成,等待发送...")
    return im


async def get_char_data(
    uid: str, char_name: str, enable_self: bool = True
) -> Union[Dict, str]:
    player_path = PLAYER_PATH / str(uid)
    SELF_PATH = player_path / "SELF"
    if "开拓者" in str(char_name):
        char_name = "开拓者"
    char_id = await name_to_avatar_id(char_name)
    if char_id == "":
        char_name = await alias_to_char_name(char_name)
    if char_name is False:
        return "请输入正确的角色名"
    char_path = player_path / f"{char_name}.json"
    char_self_path = SELF_PATH / f"{char_name}.json"
    path = Path()
    if char_path.exists():
        path = char_path
    elif enable_self and char_self_path.exists():
        path = char_self_path
    else:
        char_id_list, _ = await api_to_dict(uid, save_path=PLAYER_PATH)
        charname_list = []
        if isinstance(char_id_list, str):
            return char_id_list
        for char in char_id_list:
            charname = avatarId2Name[str(char)]
            charname_list.append(charname)
        if str(char_name) in charname_list:
            if char_path.exists():
                path = char_path
            elif enable_self and char_self_path.exists():
                path = char_self_path
        else:
            return CHAR_HINT.format(char_name, char_name)

    with Path.open(path, encoding="utf8") as fp:
        return json.load(fp)

