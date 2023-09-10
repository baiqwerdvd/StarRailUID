from typing import List, Union

import msgspec
from msgspec import Struct, field


class DamageInstanceSkill(Struct):
    skillId: int
    skillName: str
    skillEffect: str
    skillAttackType: str
    skillLevel: int


class DamageInstanceRelicSubAffix(Struct):
    SubAffixID: int
    Property: str
    Name: str
    Cnt: int
    Step: int
    Value: float


class DamageInstanceRelicMainAffix(Struct):
    AffixID: int
    Property: str
    Name: str
    Value: float


class DamageInstanceRelic(Struct):
    relicId: int
    relicName: str
    SetId: int
    SetName: str
    Type: int
    MainAffix: DamageInstanceRelicMainAffix
    SubAffixList: Union[List[DamageInstanceRelicSubAffix], None]
    Level: int = 0


class DamageInstanceWeapon(Struct):
    id_: str = field(name='id')
    level: int
    rank: int
    promotion: int


class AttributeBounsStatusAdd(Struct):
    property: str
    name: str
    value: float


class DamageInstanceAvatarAttributeBouns(Struct):
    attributeBonusId: int
    attributeBonusLevel: int
    statusAdd: AttributeBounsStatusAdd


class DamageInstanceAvatar(Struct):
    id_: str = field(name='id')
    level: int
    rank: int
    element: str
    promotion: int
    attribute_bonus: Union[List[DamageInstanceAvatarAttributeBouns], None]
    extra_ability: Union[List, None]


class DamageInstance:
    avatar: DamageInstanceAvatar
    weapon: DamageInstanceWeapon
    relic: List[DamageInstanceRelic]
    skill: List[DamageInstanceSkill]

    def __init__(self, char):
        self.avatar = DamageInstanceAvatar(
            id_=char.char_id,
            level=char.char_level,
            rank=char.char_rank,
            element=char.char_element,
            promotion=char.char_promotion,
            attribute_bonus=msgspec.convert(
                char.attribute_bonus,
                Union[List[DamageInstanceAvatarAttributeBouns], None],
            ),
            extra_ability=msgspec.convert(
                char.extra_ability, Union[List, None]
            ),
        )
        self.weapon = DamageInstanceWeapon(
            id_=char.equipment['equipmentID'],
            level=char.equipment['equipmentLevel'],
            rank=char.equipment['equipmentRank'],
            promotion=char.equipment['equipmentPromotion'],
        )
        self.relic = []
        for relic in char.char_relic:
            self.relic.append(msgspec.convert(relic, DamageInstanceRelic))
        self.skill = []
        for skill in char.char_skill:
            self.skill.append(msgspec.convert(skill, DamageInstanceSkill))
