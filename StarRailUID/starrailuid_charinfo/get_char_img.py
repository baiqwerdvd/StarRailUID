import re
import json
from pathlib import Path
from typing import Dict, Tuple, Union, Optional

from gsuid_core.logger import logger
from starrail_damage_cal.to_data import api_to_dict
from starrail_damage_cal.excel.model import (
    AvatarPromotionConfig,
    EquipmentPromotionConfig,
)

from .draw_char_img import draw_char_img
from ..utils.error_reply import CHAR_HINT
from ..utils.resource.RESOURCE_PATH import PLAYER_PATH
from ..utils.map.name_covert import (
    name_to_avatar_id,
    name_to_weapon_id,
    alias_to_char_name,
    alias_to_weapon_name,
)
from ..utils.map.SR_MAP_PATH import (
    Property2Name,
    EquipmentID2Name,
    AvatarRankSkillUp,
    EquipmentID2Rarity,
    rankId2Name,
    skillId2Name,
    avatarId2Name,
    skillId2Effect,
    avatarId2EnName,
    avatarId2Rarity,
    characterSkillTree,
    skillId2AttackType,
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
    0: ['头', '帽'],
    1: ['手'],
    2: ['衣', '服', '躯'],
    3: ['鞋', '腿'],
    4: ['球'],
    5: ['绳', '链'],
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
                char_data = await get_char_data(uid, fake_name)
                if isinstance(char_data, str):
                    char_data = await make_new_charinfo(uid, fake_name)
            else:
                char_data = await get_char_data(uid, fake_name)
            if isinstance(char_data, str):
                return char_data
            continue

        if '遗器' in part:
            char_data = await get_fake_char_data(
                char_data,
                part.replace('遗器', '').replace(changeuid, ''),
                changeuid,
            )
            if isinstance(char_data, str):
                return char_data
        else:
            for i, s in enumerate(['头部', '手部', '躯干', '腿部', '位面球', '连结绳']):
                if '赤沙' in part:
                    continue
                if part[-1] in PieceName_ilst[i]:
                    if isinstance(char_data, str):
                        return char_data
                    char_data = await change_equip(changeuid, char_data, part, s, i)
                    if not char_data:
                        change_name = part.replace(part[-1], '')
                        return f'要替换的{change_name}的{s}遗器不存在噢~'
                    break
            else:
                weapon, weapon_affix = await get_fake_weapon_str(part)

    return char_data, weapon, weapon_affix, talent_num


async def change_equip(uid: str, char_data: Dict, part: str, s: str, i: int) -> Dict:
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
    if ('魂' in char_name or '命' in char_name) and char_name[0] in CHAR_TO_INT:
        talent_num = CHAR_TO_INT[char_name[0]]
        char_name = char_name[2:]
    return char_name, talent_num


async def get_fake_weapon_str(msg: str) -> Tuple[str, Optional[int]]:
    weapon_affix = 1
    if '精' in msg and msg[1] in WEAPON_TO_INT:
        weapon_affix = WEAPON_TO_INT[msg[1]]
        weapon = msg[2:]
    else:
        weapon = msg
    return weapon, weapon_affix


async def get_fake_char_data(
    char_data: Dict, change_name: str, changeuid: str
) -> Union[Dict, str]:
    original_data = await get_char_data(changeuid, change_name)
    if isinstance(original_data, str):
        return original_data
    if isinstance(original_data, Dict):
        char_data['RelicInfo'] = original_data['RelicInfo']

    return char_data


async def get_char_data(
    uid: str, char_name: str, enable_self: bool = True
) -> Union[Dict, str]:
    player_path = PLAYER_PATH / str(uid)
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

    with Path.open(path, encoding='utf8') as fp:
        return json.load(fp)


async def make_new_charinfo(
    uid: str,
    fake_name: str,
):
    char_data = {}
    char_data['uid'] = uid
    char_data['nickName'] = 'test'
    char_id = await name_to_avatar_id(fake_name)
    if char_id == '':
        fake_name = await alias_to_char_name(fake_name)
        if fake_name is False:
            return '请输入正确的角色名'
        char_id = await name_to_avatar_id(fake_name)
    char_data['avatarId'] = int(char_id)
    char_data['avatarName'] = fake_name
    char_data['avatarElement'] = avatarId2DamageType[str(char_data['avatarId'])]
    char_data['avatarRarity'] = str(avatarId2Rarity[str(char_data['avatarId'])])
    char_data['avatarPromotion'] = 6
    char_data['avatarLevel'] = 80
    char_data['avatarSkill'] = await get_skill_list(char_data['avatarId'])
    char_data['avatarExtraAbility'] = await get_extra_list(char_data['avatarId'])
    char_data['avatarAttributeBonus'] = await get_attribute_list(char_data['avatarId'])
    char_data['RelicInfo'] = []
    char_data['avatarEnName'] = avatarId2EnName[str(char_data['avatarId'])]
    char_data['rank'] = 0
    char_data['rankList'] = []
    char_data['baseAttributes'] = await get_baseAttributes(char_data['avatarId'])
    char_data['equipmentInfo'] = {}
    return char_data


async def get_baseAttributes(
    char_id: int,
):
    # 处理基础属性
    base_attributes = {}
    avatar_promotion_base = AvatarPromotionConfig.Avatar[str(char_id)]['6']

    # 攻击力
    base_attributes['attack'] = (
        avatar_promotion_base.AttackBase.Value
        + avatar_promotion_base.AttackAdd.Value * (80 - 1)
    )
    # 防御力
    base_attributes['defence'] = (
        avatar_promotion_base.DefenceBase.Value
        + avatar_promotion_base.DefenceAdd.Value * (80 - 1)
    )
    # 血量
    base_attributes['hp'] = (
        avatar_promotion_base.HPBase.Value
        + avatar_promotion_base.HPAdd.Value * (80 - 1)
    )
    # 速度
    base_attributes['speed'] = avatar_promotion_base.SpeedBase.Value
    # 暴击率
    base_attributes['CriticalChanceBase'] = avatar_promotion_base.CriticalChance.Value
    # 暴击伤害
    base_attributes['CriticalDamageBase'] = avatar_promotion_base.CriticalDamage.Value
    # 嘲讽
    base_attributes['BaseAggro'] = avatar_promotion_base.BaseAggro.Value
    return base_attributes


async def get_attribute_list(
    char_id: int,
):
    attribute_list = []
    for attributeid in [201, 202, 203, 204, 205, 206, 207, 208, 209, 210]:
        attribute_bonus_temp = {}
        attribute_bonus_temp['attributeBonusId'] = char_id * 1000 + attributeid
        attribute_bonus_temp['attributeBonusLevel'] = 1
        status_add = characterSkillTree[str(char_id)][
            str(attribute_bonus_temp['attributeBonusId'])
        ]['levels'][0]['properties']
        attribute_bonus_temp['statusAdd'] = {}
        if status_add:
            for property_ in status_add:
                attribute_bonus_temp['statusAdd']['property'] = property_['type']
                attribute_bonus_temp['statusAdd']['name'] = Property2Name[
                    property_['type']
                ]
                attribute_bonus_temp['statusAdd']['value'] = property_['value']
                attribute_list.append(attribute_bonus_temp)
    return attribute_list


async def get_extra_list(
    char_id: int,
):
    extra_list = []
    for extraid in [101, 102, 103]:
        extra_temp = {}
        extra_temp['extraAbilityId'] = char_id * 1000 + extraid
        extra_temp['extraAbilityLevel'] = 1
        extra_list.append(extra_temp)
    return extra_list


async def get_skill_list(
    char_id: int,
):
    Skilllist = []
    for skillid in [1, 2, 3, 4, 7]:
        skill_temp = {}
        skill_temp['skillId'] = char_id * 100 + skillid
        skill_temp['skillName'] = skillId2Name[str(skill_temp['skillId'])]
        skill_temp['skillEffect'] = skillId2Effect[str(skill_temp['skillId'])]
        skill_temp['skillAttackType'] = skillId2AttackType[str(skill_temp['skillId'])]
        skilllevel = 10
        if skillid == 1:
            skilllevel = 6
        if skillid == 7:
            skilllevel = 1
        skill_temp['skillLevel'] = skilllevel
        Skilllist.append(skill_temp)
    return Skilllist


async def get_rank_list(
    char_id: str,
    talent_num: int,
):
    rank_temp = []
    for index in range(talent_num):
        rankTemp = {}
        rank_id = int(str(char_id) + '0' + str(index + 1))
        rankTemp['rankId'] = rank_id
        rankTemp['rankName'] = rankId2Name[str(rank_id)]
        rank_temp.append(rankTemp)
    return rank_temp


async def get_char(
    char_data: dict,
    weapon: Optional[str] = None,
    weapon_affix: Optional[int] = None,
    talent_num: Optional[int] = None,
):
    if isinstance(talent_num, int):
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

        # 处理命座中的 level_up_skills
        if char_data.get('rankList'):
            for rank_item in char_data['rankList']:
                rank_id = rank_item['rankId']
                level_up_skill = AvatarRankSkillUp[str(rank_id)]
                if level_up_skill:
                    for item in level_up_skill:
                        skill_id = item['id']
                        skill_up_num = item['num']
                        # 查找skill_id在不在avatarSkill中
                        for index, skill_item in enumerate(char_data['avatarSkill']):
                            if str(skill_id) == str(skill_item['skillId']):
                                if skill_id[-1] == 1:
                                    skilllevel_max = 7
                                else:
                                    skilllevel_max = 12
                                skilllevel = min(
                                    skilllevel_max,
                                    char_data['avatarSkill'][index]['skillLevel']
                                    + skill_up_num,
                                )
                                char_data['avatarSkill'][index][
                                    'skillLevel'
                                ] = skilllevel
                                break

    if isinstance(weapon, str):
        # 处理武器
        equipmentid = await name_to_weapon_id(weapon)
        if equipmentid == '':
            weapon = await alias_to_weapon_name(weapon)
            equipmentid = await name_to_weapon_id(weapon)
        equipment_info = {}
        equipment_info['equipmentID'] = int(equipmentid)
        equipment_info['equipmentName'] = EquipmentID2Name[str(equipmentid)]

        equipment_info['equipmentLevel'] = 80
        equipment_info['equipmentPromotion'] = 6
        equipment_info['equipmentRank'] = weapon_affix
        equipment_info['equipmentRarity'] = EquipmentID2Rarity[str(equipmentid)]
        equipment_base_attributes = {}
        equipment_promotion_base = EquipmentPromotionConfig.Equipment[str(equipmentid)][
            '6'
        ]

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
