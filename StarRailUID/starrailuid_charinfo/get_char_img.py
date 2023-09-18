import re
import json
from pathlib import Path
from typing import Dict, Tuple, Union, Optional

from gsuid_core.logger import logger

from .to_data import api_to_dict
from .draw_char_img import draw_char_img
from ..utils.error_reply import CHAR_HINT
from ..utils.resource.RESOURCE_PATH import PLAYER_PATH
from ..utils.excel.model import EquipmentPromotionConfig
from ..utils.map.name_covert import (
    name_to_avatar_id,
    name_to_weapon_id,
    alias_to_char_name,
)
from ..utils.map.SR_MAP_PATH import (
    EquipmentID2Name,
    EquipmentID2Rarity,
    rankId2Name,
    avatarId2Name,
    avatarId2EnName,
    avatarId2DamageType,
)

WEAPON_TO_INT = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '满': 5,
}

CHAR_TO_INT = {
    '零': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '满': 6,
}

PieceName_ilst = {
    0: ['头', '帽子', '头部'],
    1: ['手', '手套', '手部'],
    2: ['衣', '衣服', '躯干'],
    3: ['鞋', '鞋子', '腿', '腿部'],
    4: ['球', '位面球'],
    5: ['绳', '绳子', '链', '链子', '连结绳'],
}


async def draw_char_info_img(raw_mes: str, sr_uid: str):
    # 获取角色名
    # msg = ' '.join(re.findall('[\u4e00-\u9fa5]+', raw_mes))
    _args = await get_char_args(raw_mes, sr_uid)
    if isinstance(_args, str):
        return _args
    if isinstance(_args[0], str):
        return _args[0]

    char = await get_char(*_args)

    if isinstance(char, str):
        logger.info('[sr查询角色] 绘图失败, 替换的武器不正确!')
        return char

    im = await draw_char_img(char, sr_uid, raw_mes)
    logger.info('[查询角色] 绘图完成,等待发送...')
    return im


async def get_char_args(
    msg: str, uid: str
) -> Union[Tuple[Dict, Optional[str], Optional[int], Optional[int]], str]:
    # 可能进来的值
    # 六命希儿带于夜色中换1000xxxx4青雀遗器换1000xxxx6希儿头换银狼手
    # 六命希儿带于夜色中换1000xxxx6希儿头
    # 希儿换银狼手
    fake_name = ''
    talent_num = None
    char_data = {}
    weapon, weapon_affix = None, None

    msg = (
        msg.replace('带', '换')
        .replace('拿', '换')
        .replace('圣遗物', '遗器')
        .replace('命', '魂')
    )

    # 希儿带于夜色中换1000xxxx6希儿头
    msg_list = msg.split('换')
    for index, part in enumerate(msg_list):
        changeuid = await get_part_uid(part, uid)
        if changeuid is None:
            return 'UID不正确噢~'
        # 判断主体
        if index == 0:
            fake_name, talent_num = await get_fake_char_str(part)
            # 判断是否开启fake_char
            if '遗器' in msg:
                char_data = await get_fake_char_data(
                    char_data, fake_name, changeuid
                )
            else:
                char_data = await get_char_data(uid, fake_name)
            if isinstance(char_data, str):
                return char_data
            continue

        if '遗器' in part:
            fake_data = await get_char_data(
                changeuid, part.replace('遗器', '').replace(changeuid, '')
            )
            if isinstance(fake_data, str):
                return fake_data
            char_data = await get_fake_char_data(fake_data, fake_name, uid)
            if isinstance(char_data, str):
                return char_data
        else:
            for i, s in enumerate(['头部', '手部', '躯干', '腿部', '位面球', '连结绳']):
                if '赤沙' in part:
                    continue
                if part[-1] in PieceName_ilst[i]:
                    if isinstance(char_data, str):
                        return char_data
                    char_data = await change_equip(
                        changeuid, char_data, part, s, i
                    )
                    if not char_data:
                        return '要替换的部件不存在噢~'
                    break
            else:
                weapon, weapon_affix = await get_fake_weapon_str(part)

    return char_data, weapon, weapon_affix, talent_num


async def change_equip(
    uid: str, char_data: Dict, part: str, s: str, i: int
) -> Dict:
    char_name = part.replace(part[-1], '').replace(uid, '')
    fake_data = await get_char_data(uid, char_name)
    if isinstance(fake_data, str):
        return {}
    relicmap = i + 1
    for equip in fake_data['RelicInfo']:
        if str(str(equip['relicId'])[-1]) == str(relicmap):
            char_data['RelicInfo'][i] = equip
            break
    return char_data


async def get_part_uid(part: str, uid: str):
    sr_uid = uid
    uid_data = re.findall(r'\d{9}', part)
    if uid_data:
        sr_uid: Optional[str] = uid_data[0]
    return sr_uid


async def get_fake_char_str(char_name: str) -> Tuple[str, Optional[int]]:
    """
    获取一个角色信息

    """
    talent_num = None
    if '魂' in char_name and char_name[0] in CHAR_TO_INT:
        talent_num = CHAR_TO_INT[char_name[0]]
        char_name = char_name[2:]
    return char_name, talent_num


async def get_fake_weapon_str(msg: str) -> Tuple[str, Optional[int]]:
    weapon_affix = 0
    if '精' in msg and msg[1] in WEAPON_TO_INT:
        weapon_affix = WEAPON_TO_INT[msg[1]]
        weapon = msg[2:]
    else:
        weapon = msg
    return weapon, weapon_affix


async def get_fake_char_data(
    char_data: Dict, fake_name: str, uid: str
) -> Union[Dict, str]:
    fake_name = await alias_to_char_name(fake_name)
    original_data = await get_char_data(uid, fake_name)
    if isinstance(original_data, str):
        return original_data
    if isinstance(original_data, Dict):
        char_data['RelicInfo'] = original_data['RelicInfo']
        char_data['avatarAttributeBonus'] = original_data[
            'avatarAttributeBonus'
        ]
        char_data['rankList'] = original_data['rankList']
        char_data['avatarSkill'] = original_data['avatarSkill']
        char_data['avatarExtraAbility'] = original_data['avatarExtraAbility']
        char_data['equipmentInfo'] = original_data['equipmentInfo']
        char_data['baseAttributes'] = original_data['baseAttributes']
    char_data['uid'] = original_data['uid']
    char_data['rank'] = original_data['rank']
    char_data['nickName'] = original_data['nickName']
    char_data['avatarRarity'] = original_data['avatarRarity']
    char_data['avatarPromotion'] = original_data['avatarPromotion']
    char_data['avatarName'] = fake_name
    char_data['avatarId'] = await name_to_avatar_id(fake_name)
    en_name: str = avatarId2EnName(char_data['avatarId'])  # type: ignore
    char_data['avatarEnName'] = en_name
    if str(char_data['avatarId']) in avatarId2DamageType:
        char_data['avatarElement'] = avatarId2DamageType[
            str(char_data['avatarId'])
        ]
    else:
        return '要查询的角色不存在...'
    char_data['avatarLevel'] = '80'

    return char_data


async def get_char_data(
    sr_uid: str, char_name: str, enable_self: bool = True
) -> Union[Dict, str]:
    player_path = PLAYER_PATH / str(sr_uid)
    SELF_PATH = player_path / 'SELF'
    if '开拓者' in str(char_name):
        char_name = '开拓者'
    char_id = await name_to_avatar_id(char_name)
    if char_id == '':
        char_name = await alias_to_char_name(char_name)
    if char_name is False:
        return '请输入正确的角色名'
    char_path = player_path / f'{char_name}.json'
    char_self_path = SELF_PATH / f'{char_name}.json'
    path = Path()
    if char_path.exists():
        path = char_path
    elif enable_self and char_self_path.exists():
        path = char_self_path
    else:
        char_data_list = await api_to_dict(sr_uid)
        charname_list = []
        if isinstance(char_data_list, str):
            return char_data_list
        for char in char_data_list:
            charname = avatarId2Name[str(char)]
            charname_list.append(charname)
        if str(char_name) in charname_list:
            if char_path.exists():
                path = char_path
            elif enable_self and char_self_path.exists():
                path = char_self_path
        else:
            return CHAR_HINT.format(char_name, char_name)

    with Path.open(path, encoding='utf8') as fp:
        return json.load(fp)


async def get_char(
    char_data: dict,
    weapon: Optional[str] = None,
    weapon_affix: Optional[int] = None,
    talent_num: Optional[int] = None,
):
    if talent_num:
        # 处理命座
        rank_temp = []
        char_data['rank'] = talent_num
        for index in range(talent_num):
            rankTemp = {}
            rank_id = int(str(char_data['avatarId']) + '0' + str(index + 1))
            rankTemp['rankId'] = rank_id
            rankTemp['rankName'] = rankId2Name[str(rank_id)]
            rank_temp.append(rankTemp)
        char_data['rankList'] = rank_temp
    if weapon:
        # 处理武器
        equipmentid = await name_to_weapon_id(weapon)
        equipment_info = {}
        equipment_info['equipmentID'] = int(equipmentid)
        equipment_info['equipmentName'] = EquipmentID2Name[str(equipmentid)]

        equipment_info['equipmentLevel'] = 80
        equipment_info['equipmentPromotion'] = 6
        equipment_info['equipmentRank'] = weapon_affix
        equipment_info['equipmentRarity'] = EquipmentID2Rarity[
            str(equipmentid)
        ]
        equipment_base_attributes = {}
        equipment_promotion_base = EquipmentPromotionConfig.Equipment[
            str(equipmentid)
        ]['6']

        # 生命值
        equipment_base_attributes['hp'] = (
            equipment_promotion_base.BaseHP.Value
            + equipment_promotion_base.BaseHPAdd.Value * (80 - 1)
        )
        # 攻击力
        equipment_base_attributes['attack'] = (
            equipment_promotion_base.BaseAttack.Value
            + equipment_promotion_base.BaseAttackAdd.Value * (80 - 1)
        )
        # 防御力
        equipment_base_attributes['defence'] = (
            equipment_promotion_base.BaseDefence.Value
            + equipment_promotion_base.BaseDefenceAdd.Value * (80 - 1)
        )
        equipment_info['baseAttributes'] = equipment_base_attributes

        char_data['equipmentInfo'] = equipment_info
    return char_data
