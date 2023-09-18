from typing import Dict, List, Union

from msgspec import Struct

from .read_excel import (
    RelicSubAffix,
    RelicMainAffix,
    AvatarPromotion,
    EquipmentPromotion,
)


class PromotionCost(Struct):
    ItemID: int
    ItemNum: int


class PromotionAttr(Struct):
    Value: float


class SingleAvatarPromotion(Struct):
    AvatarID: int
    Promotion: int
    PromotionCostList: List[PromotionCost]
    MaxLevel: int
    PlayerLevelRequire: Union[int, None]
    WorldLevelRequire: Union[int, None]
    AttackBase: PromotionAttr
    AttackAdd: PromotionAttr
    DefenceBase: PromotionAttr
    DefenceAdd: PromotionAttr
    HPBase: PromotionAttr
    HPAdd: PromotionAttr
    SpeedBase: PromotionAttr
    CriticalChance: PromotionAttr
    CriticalDamage: PromotionAttr
    BaseAggro: PromotionAttr


class SingleEquipmentPromotion(Struct):
    EquipmentID: int
    Promotion: int
    PromotionCostList: List[PromotionCost]
    MaxLevel: int
    PlayerLevelRequire: Union[int, None]
    WorldLevelRequire: Union[int, None]
    BaseHP: PromotionAttr
    BaseHPAdd: PromotionAttr
    BaseAttack: PromotionAttr
    BaseAttackAdd: PromotionAttr
    BaseDefence: PromotionAttr
    BaseDefenceAdd: PromotionAttr


class SingleRelicMainAffix(Struct):
    GroupID: int
    AffixID: int
    Property: str
    BaseValue: PromotionAttr
    LevelAdd: PromotionAttr
    IsAvailable: bool


class SingleRelicSubAffix(Struct):
    GroupID: int
    AffixID: int
    Property: str
    BaseValue: PromotionAttr
    StepValue: PromotionAttr
    StepNum: int


class AvatarPromotionConfigModel(Struct):
    Avatar: Dict[str, Dict[str, SingleAvatarPromotion]]

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            Avatar={
                avatar_id: {
                    promotion: SingleAvatarPromotion(
                        AvatarID=promotion_dict[promotion]['AvatarID'],
                        Promotion=promotion_dict[promotion]['Promotion'],
                        PromotionCostList=[
                            PromotionCost(
                                ItemID=item['ItemID'], ItemNum=item['ItemNum']
                            )
                            for item in promotion_dict[promotion][
                                'PromotionCostList'
                            ]
                        ],
                        PlayerLevelRequire=promotion_dict[promotion].get(
                            'PlayerLevelRequire', None
                        ),
                        WorldLevelRequire=promotion_dict[promotion].get(
                            'WorldLevelRequire', None
                        ),
                        MaxLevel=promotion_dict[promotion]['MaxLevel'],
                        AttackBase=PromotionAttr(
                            Value=promotion_dict[promotion]['AttackBase'][
                                'Value'
                            ]
                        ),
                        AttackAdd=PromotionAttr(
                            Value=promotion_dict[promotion]['AttackAdd'][
                                'Value'
                            ]
                        ),
                        DefenceBase=PromotionAttr(
                            Value=promotion_dict[promotion]['DefenceBase'][
                                'Value'
                            ]
                        ),
                        DefenceAdd=PromotionAttr(
                            Value=promotion_dict[promotion]['DefenceAdd'][
                                'Value'
                            ]
                        ),
                        HPBase=PromotionAttr(
                            Value=promotion_dict[promotion]['HPBase']['Value']
                        ),
                        HPAdd=PromotionAttr(
                            Value=promotion_dict[promotion]['HPAdd']['Value']
                        ),
                        SpeedBase=PromotionAttr(
                            Value=promotion_dict[promotion]['SpeedBase'][
                                'Value'
                            ]
                        ),
                        CriticalChance=PromotionAttr(
                            Value=promotion_dict[promotion]['CriticalChance'][
                                'Value'
                            ]
                        ),
                        CriticalDamage=PromotionAttr(
                            Value=promotion_dict[promotion]['CriticalDamage'][
                                'Value'
                            ]
                        ),
                        BaseAggro=PromotionAttr(
                            Value=promotion_dict[promotion]['BaseAggro'][
                                'Value'
                            ]
                        ),
                    )
                    for promotion in promotion_dict.keys()
                }
                for avatar_id, promotion_dict in data.items()
            }
        )


class EquipmentPromotionConfigModel(Struct):
    Equipment: Dict[str, Dict[str, SingleEquipmentPromotion]]

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            Equipment={
                equipment_id: {
                    promotion: SingleEquipmentPromotion(
                        EquipmentID=promotion_dict[promotion]['EquipmentID'],
                        Promotion=promotion_dict[promotion]['Promotion'],
                        PromotionCostList=[
                            PromotionCost(
                                ItemID=item['ItemID'], ItemNum=item['ItemNum']
                            )
                            for item in promotion_dict[promotion][
                                'PromotionCostList'
                            ]
                        ],
                        PlayerLevelRequire=promotion_dict[promotion].get(
                            'PlayerLevelRequire', None
                        ),
                        WorldLevelRequire=promotion_dict[promotion].get(
                            'WorldLevelRequire', None
                        ),
                        MaxLevel=promotion_dict[promotion]['MaxLevel'],
                        BaseHP=PromotionAttr(
                            Value=promotion_dict[promotion]['BaseHP']['Value']
                        ),
                        BaseHPAdd=PromotionAttr(
                            Value=promotion_dict[promotion]['BaseHPAdd'][
                                'Value'
                            ]
                        ),
                        BaseAttack=PromotionAttr(
                            Value=promotion_dict[promotion]['BaseAttack'][
                                'Value'
                            ]
                        ),
                        BaseAttackAdd=PromotionAttr(
                            Value=promotion_dict[promotion]['BaseAttackAdd'][
                                'Value'
                            ]
                        ),
                        BaseDefence=PromotionAttr(
                            Value=promotion_dict[promotion]['BaseDefence'][
                                'Value'
                            ]
                        ),
                        BaseDefenceAdd=PromotionAttr(
                            Value=promotion_dict[promotion]['BaseDefenceAdd'][
                                'Value'
                            ]
                        ),
                    )
                    for promotion in promotion_dict.keys()
                }
                for equipment_id, promotion_dict in data.items()
            }
        )


class RelicMainAffixConfigModel(Struct):
    Relic: Dict[str, Dict[str, SingleRelicMainAffix]]

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            Relic={
                relic_id: {
                    group_id: SingleRelicMainAffix(
                        GroupID=affix_dict[group_id]['GroupID'],
                        AffixID=affix_dict[group_id]['AffixID'],
                        Property=affix_dict[group_id]['Property'],
                        BaseValue=PromotionAttr(
                            Value=affix_dict[group_id]['BaseValue']['Value']
                        ),
                        LevelAdd=PromotionAttr(
                            Value=affix_dict[group_id]['LevelAdd']['Value']
                        ),
                        IsAvailable=affix_dict[group_id]['IsAvailable'],
                    )
                    for group_id in affix_dict.keys()
                }
                for relic_id, affix_dict in data.items()
            }
        )


class RelicSubAffixConfigModel(Struct):
    Relic: Dict[str, Dict[str, SingleRelicSubAffix]]

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            Relic={
                relic_id: {
                    group_id: SingleRelicSubAffix(
                        GroupID=affix_dict[group_id]['GroupID'],
                        AffixID=affix_dict[group_id]['AffixID'],
                        Property=affix_dict[group_id]['Property'],
                        BaseValue=PromotionAttr(
                            Value=affix_dict[group_id]['BaseValue']['Value']
                        ),
                        StepValue=PromotionAttr(
                            Value=affix_dict[group_id]['StepValue']['Value']
                        ),
                        StepNum=affix_dict[group_id]['StepNum'],
                    )
                    for group_id in affix_dict.keys()
                }
                for relic_id, affix_dict in data.items()
            }
        )


AvatarPromotionConfig = AvatarPromotionConfigModel.from_json(AvatarPromotion)
EquipmentPromotionConfig = EquipmentPromotionConfigModel.from_json(
    EquipmentPromotion
)
RelicMainAffixConfig = RelicMainAffixConfigModel.from_json(RelicMainAffix)
RelicSubAffixConfig = RelicSubAffixConfigModel.from_json(RelicSubAffix)
