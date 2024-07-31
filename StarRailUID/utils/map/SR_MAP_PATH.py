import json
from pathlib import Path
from typing import Dict, List, Optional, TypedDict, Union

from ...version import StarRail_version

from msgspec import Struct, convert, json as msgjson


class RelicSetStatusAdd(Struct):
    Property: str
    Value: float


MAP = Path(__file__).parent / 'data'

version = StarRail_version

avatarId2Name_fileName = f'avatarId2Name_mapping_{version}.json'
avatarId2EnName_fileName = f'avatarId2EnName_mapping_{version}.json'
EquipmentID2Name_fileName = f'EquipmentID2Name_mapping_{version}.json'
EquipmentID2EnName_fileName = f'EquipmentID2EnName_mapping_{version}.json'
skillId2Name_fileName = f'skillId2Name_mapping_{version}.json'
skillId2Type_fileName = f'skillId2Type_mapping_{version}.json'
Property2Name_fileName = f'Property2Name_mapping_{version}.json'
RelicId2SetId_fileName = f'RelicId2SetId_mapping_{version}.json'
SetId2Name_fileName = f'SetId2Name_mapping_{version}.json'
rankId2Name_fileName = f'rankId2Name_mapping_{version}.json'
characterSkillTree_fileName = f'characterSkillTree_mapping_{version}.json'
avatarId2DamageType_fileName = f'avatarId2DamageType_mapping_{version}.json'
avatarId2Rarity_fileName = f'avatarId2Rarity_mapping_{version}.json'
EquipmentID2AbilityProperty_fileName = (
    f'EquipmentID2AbilityProperty_mapping_{version}.json'
)
RelicSetSkill_fileName = f'RelicSetSkill_mapping_{version}.json'
skillId2AttackType_fileName = f'skillId2AttackType_mapping_{version}.json'
EquipmentID2Rarity_fileName = f'EquipmentID2Rarity_mapping_{version}.json'
RelicId2Rarity_fileName = f'RelicId2Rarity_mapping_{version}.json'
ItemId2Name_fileName = f'ItemId2Name_mapping_{version}.json'
RelicId2MainAffixGroup_fileName = (
    f'RelicId2MainAffixGroup_mapping_{version}.json'
)
AvatarRelicScore_fileName = 'AvatarRelicScore.json'
avatarRankSkillUp_fileName = f'avatarRankSkillUp_mapping_{version}.json'


class TS(TypedDict):
    Name: Dict[str, str]
    Icon: Dict[str, str]


class LU(TypedDict):
    id: str
    num: int


with Path.open(MAP / avatarId2Name_fileName, encoding='UTF-8') as f:
    avatarId2Name = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / avatarId2EnName_fileName, encoding='UTF-8') as f:
    avatarId2EnName = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / EquipmentID2Name_fileName, encoding='UTF-8') as f:
    EquipmentID2Name = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / EquipmentID2EnName_fileName, encoding='UTF-8') as f:
    EquipmentID2EnName = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / skillId2Name_fileName, encoding='UTF-8') as f:
    skillId2Name = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / skillId2Type_fileName, encoding='UTF-8') as f:
    skillId2Effect = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / Property2Name_fileName, encoding='UTF-8') as f:
    Property2Name = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / RelicId2SetId_fileName, encoding='UTF-8') as f:
    RelicId2SetId = msgjson.decode(f.read(), type=Dict[str, int])

with Path.open(MAP / SetId2Name_fileName, encoding='UTF-8') as f:
    SetId2Name = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / rankId2Name_fileName, encoding='UTF-8') as f:
    rankId2Name = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / characterSkillTree_fileName, encoding='UTF-8') as f:
    characterSkillTree = msgjson.decode(f.read(), type=Dict[str, Dict])

with Path.open(MAP / avatarId2DamageType_fileName, encoding='UTF-8') as f:
    avatarId2DamageType = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / 'char_alias.json', encoding='UTF-8') as f:
    alias_data = msgjson.decode(f.read(), type=Dict[str, Dict[str, List]])

with Path.open(MAP / avatarId2Rarity_fileName, encoding='UTF-8') as f:
    avatarId2Rarity = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(
    MAP / EquipmentID2AbilityProperty_fileName, encoding='UTF-8'
) as f:
    EquipmentID2AbilityProperty = msgjson.decode(
        f.read(), type=Dict[str, Dict[str, List]]
    )

# with Path.open(MAP / RelicSetSkill_fileName, encoding='UTF-8') as f:
#     RelicSetSkill = convert(json.load(f), Dict[str, Dict[str, object]])
#     print(RelicSetSkill)

with Path.open(MAP / skillId2AttackType_fileName, encoding='UTF-8') as f:
    skillId2AttackType = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / EquipmentID2Rarity_fileName, encoding='UTF-8') as f:
    EquipmentID2Rarity = msgjson.decode(f.read(), type=Dict[str, int])

with Path.open(MAP / RelicId2Rarity_fileName, encoding='UTF-8') as f:
    RelicId2Rarity = msgjson.decode(f.read(), type=Dict[str, int])

with Path.open(MAP / ItemId2Name_fileName, encoding='UTF-8') as f:
    ItemId2Name = msgjson.decode(f.read(), type=Dict[str, str])

with Path.open(MAP / RelicId2MainAffixGroup_fileName, encoding='UTF-8') as f:
    RelicId2MainAffixGroup = msgjson.decode(f.read(), type=Dict[str, int])

with Path.open(MAP / AvatarRelicScore_fileName, encoding='UTF-8') as f:
    AvatarRelicScore = msgjson.decode(f.read(), type=List[Dict])

with Path.open(MAP / avatarRankSkillUp_fileName, encoding='UTF-8') as f:
    AvatarRankSkillUp = msgjson.decode(
        f.read(), type=Dict[str, Union[List[LU], None]]
    )
