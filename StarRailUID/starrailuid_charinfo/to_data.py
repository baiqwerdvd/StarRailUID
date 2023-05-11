import json
from typing import List, Union, Optional

from mpmath import mp
from httpx import ReadTimeout
from gsuid_core.utils.api.enka.models import EnkaData

from ..utils.error_reply import UID_HINT
from ..utils.excel.read_excel import AvatarPromotion
from ..utils.resource.RESOURCE_PATH import PLAYER_PATH
from ..sruid_utils.api.lulu.requests import get_char_card_info

# from gsuid_core.utils.api.minigg.request import get_weapon_info
from .cal_value import cal_relic_sub_affix, cal_relic_main_affix
from ..utils.map.SR_MAP_PATH import (
    SetId2Name,
    Property2Name,
    RelicId2SetId,
    EquipmentID2Name,
    rankId2Name,
    skillId2Name,
    skillId2Type,
    avatarId2Name,
    avatarId2EnName,
)

mp.dps = 14

PROP_ATTR_MAP = {
    'Anemo': '44',
    'Cryo': '46',
    'Dendro': '43',
    'Electro': '41',
    'Geo': '45',
    'Hydro': '42',
    'Pyro': '40',
}


async def enka_to_dict(
    sr_uid: str, sr_data: Optional[EnkaData] = None
) -> Union[List[dict], str]:
    """
    :说明:
      访问luluAPI并转换为StarRailUID的数据Json。
    :参数:
      * ``uid: str``: 玩家uid。
      * ``sr_data: Optional[dict] = None``: 来自lulu的dict, 可留空。
    :返回:
      * ``刷新完成提示语: str``: 包含刷新成功的角色列表。
    """
    if '未找到绑定的UID' in sr_uid:
        return UID_HINT
    if sr_data:
        pass
    else:
        try:
            sr_data = await get_char_card_info(sr_uid)
        except ReadTimeout:
            return '网络不太稳定...'
    if isinstance(sr_data, str):
        return []
    if isinstance(sr_data, dict):
        if 'PlayerDetailInfo' not in sr_data:
            print(sr_data)
            im = '服务器正在维护或者关闭中...\n检查lulu api是否可以访问\n如可以访问,尝试上报Bug!'
            return im
    elif sr_data is None:
        return []

    PlayerDetailInfo = sr_data['PlayerDetailInfo']
    path = PLAYER_PATH / str(sr_uid)
    path.mkdir(parents=True, exist_ok=True)
    with open(
        path / '{}.json'.format(str(sr_uid)), 'w', encoding='UTF-8'
    ) as file:
        json.dump(PlayerDetailInfo, file, ensure_ascii=False)
    with open(path / 'rawData.json', 'w', encoding='UTF-8') as file:
        json.dump(sr_data, file, ensure_ascii=False)

    if 'PlayerDetailInfo' not in sr_data:
        return f'SR_UID{sr_uid}刷新失败！未打开角色展柜!'

    char_dict_list = []
    im = f'UID: {sr_uid} 的角色展柜刷新成功\n刷新角色如下: '
    if PlayerDetailInfo['IsDisplayAvatarList']:
        for char in PlayerDetailInfo['DisplayAvatarList']:
            char_dict, avatarName = await get_data(char, sr_data, sr_uid)
            im += f'{avatarName} '
            char_dict_list.append(char_dict)
    else:
        char_dict, avatarName = await get_data(
            PlayerDetailInfo['AssistAvatar'], sr_data, sr_uid
        )
        im += f'{avatarName} '
        char_dict_list.append(char_dict)

    return im


async def get_data(char: dict, sr_data: dict, sr_uid: str):
    PlayerDetailInfo = sr_data['PlayerDetailInfo']
    path = PLAYER_PATH / str(sr_uid)
    # 处理基本信息
    char_data = {
        'uid': str(sr_uid),
        'nickName': PlayerDetailInfo['NickName'],
        'avatarId': char['AvatarID'],
        'avatarName': avatarId2Name[str(char['AvatarID'])],
        'avatarPromotion': char['Promotion'],
        'avatarLevel': char['Level'],
        'avatarSkill': [],
        'RelicInfo': [],
        'avatarFightProp': {},
    }
    avatarName = avatarId2Name[str(char['AvatarID'])]

    # 处理技能
    for behavior in char['BehaviorList']:
        if f'{char["AvatarID"]}0' in str(behavior['BehaviorID']):
            skill_temp = {}
            skill_temp['skillId'] = (
                char['AvatarID'] * 100 + behavior['BehaviorID'] % 10
            )
            skill_temp['skillName'] = skillId2Name[str(skill_temp['skillId'])]
            skill_temp['skillType'] = skillId2Type[str(skill_temp['skillId'])]
            skill_temp['skillLevel'] = behavior['Level']
            #     behavior_temp['skillIcon'] = skillId2Name['Icon'][
            #         behavior_temp['skillId']
            #     ]
            char_data['avatarSkill'].append(skill_temp)

    char_data['avatarEnName'] = avatarId2EnName[str(char['AvatarID'])]

    # 处理遗器
    for relic in char['RelicList']:
        relic_temp = {}
        relic_temp['relicId'] = relic['ID']
        relic_temp['SetId'] = int(RelicId2SetId[str(relic['ID'])])
        relic_temp['name'] = SetId2Name[str(relic_temp['SetId'])]
        relic_temp['Level'] = relic['Level'] if 'Level' in relic else 1
        relic_temp['Type'] = relic['Type']

        relic_temp['MainAffix'] = {}
        relic_temp['MainAffix']['AffixID'] = relic['MainAffixID']
        affix_property, value = await cal_relic_main_affix(
            relic_id=relic['ID'],
            affix_id=relic['MainAffixID'],
            relic_type=relic['Type'],
            relic_level=relic_temp['Level'],
        )
        relic_temp['MainAffix']['Property'] = affix_property
        relic_temp['MainAffix']['Name'] = Property2Name[affix_property]
        relic_temp['MainAffix']['Value'] = value

        relic_temp['SubAffixList'] = []
        for sub_affix in relic['RelicSubAffix']:
            sub_affix_temp = {}
            sub_affix_temp['SubAffixID'] = sub_affix['SubAffixID']
            sub_affix_property, value = await cal_relic_sub_affix(
                relic_id=relic['ID'],
                affix_id=sub_affix['SubAffixID'],
                cnt=sub_affix['Cnt'],
                step=sub_affix['Step'] if 'Step' in sub_affix else 0,
            )
            sub_affix_temp['Property'] = sub_affix_property
            sub_affix_temp['Name'] = Property2Name[sub_affix_property]
            sub_affix_temp['Cnt'] = sub_affix['Cnt']
            sub_affix_temp['Step'] = (
                sub_affix['Step'] if 'Step' in sub_affix else 0
            )
            sub_affix_temp['Value'] = value
            relic_temp['SubAffixList'].append(sub_affix_temp)
        char_data['RelicInfo'].append(relic_temp)

    # 处理命座
    rank_temp = []
    if 'Rank' in char:
        char_data['rank'] = char['Rank']
        for index in range(char['Rank']):
            rankTemp = {}
            rank_id = int(str(char['AvatarID']) + '0' + str(index + 1))
            rankTemp['rankId'] = rank_id
            rankTemp['rankName'] = rankId2Name[str(rank_id)]
            rank_temp.append(rankTemp)
        char_data['rankList'] = rank_temp

    # 处理基础属性
    base_attributes = {}
    avatar_promotion_base = AvatarPromotion[str(char['AvatarID'])][
        str(char['Promotion'])
    ]

    # 攻击力
    base_attributes['attack'] = str(
        mp.mpf(avatar_promotion_base["AttackBase"]['Value'])
        + mp.mpf(avatar_promotion_base["AttackAdd"]['Value'])
        * (char['Level'] - 1)
    )
    # 防御力
    base_attributes['defence'] = str(
        mp.mpf(avatar_promotion_base["DefenceBase"]['Value'])
        + mp.mpf(avatar_promotion_base["DefenceAdd"]['Value'])
        * (char['Level'] - 1)
    )
    # 血量
    base_attributes['hp'] = str(
        mp.mpf(avatar_promotion_base["HPBase"]['Value'])
        + mp.mpf(avatar_promotion_base["HPAdd"]['Value']) * (char['Level'] - 1)
    )
    # 速度
    base_attributes['speed'] = str(
        mp.mpf(avatar_promotion_base["SpeedBase"]['Value'])
    )
    # 暴击率
    base_attributes['CriticalChance'] = str(
        mp.mpf(avatar_promotion_base["CriticalChance"]['Value'])
    )
    # 暴击伤害
    base_attributes['CriticalDamage'] = str(
        mp.mpf(avatar_promotion_base["CriticalDamage"]['Value'])
    )
    # 嘲讽
    base_attributes['BaseAggro'] = str(
        mp.mpf(avatar_promotion_base["BaseAggro"]['Value'])
    )

    char_data['base_attributes'] = base_attributes

    # 处理武器

    equipment_info = {}

    equipment_info['equipmentID'] = char['EquipmentID']['ID']
    equipment_info['equipmentName'] = EquipmentID2Name[
        str(equipment_info['equipmentID'])
    ]
    # equipment_info['EquipmentStar'] = equipment_info['flat']['rankLevel']

    equipment_info['equipmentLevel'] = char['EquipmentID']['Level']
    equipment_info['equipmentPromotion'] = char['EquipmentID']['Promotion']
    equipment_info['equipmentRank'] = char['EquipmentID']['Rank']
    char_data['equipmentInfo'] = equipment_info

    with open(
        path / '{}.json'.format(avatarName), 'w', encoding='UTF-8'
    ) as file:
        json.dump(char_data, file, ensure_ascii=False)
    return char_data, avatarName


async def enka_to_data(
    uid: str, enka_data: Optional[EnkaData] = None
) -> Union[dict, str]:
    raw_data = await enka_to_dict(uid, enka_data)
    if isinstance(raw_data, str):
        return raw_data
    char_name_list = []
    char_name_list_str = ''
    for char_data in raw_data:
        char_name_list.append(char_data['avatarName'])
    char_name_list_str = ','.join(char_name_list)
    return f'UID{uid}刷新完成！\n本次缓存：{char_name_list_str}'
