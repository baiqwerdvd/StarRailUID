from typing import List, Union

from msgspec import Struct, convert

from .read_excel import (
    AvatarPromotion,
    EquipmentPromotion,
    RelicMainAffix,
    RelicSubAffix,
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


AvatarPromotionConfig = convert(AvatarPromotion, List[SingleAvatarPromotion])
EquipmentPromotionConfig = convert(EquipmentPromotion, List[SingleEquipmentPromotion])
RelicMainAffixConfig = convert(RelicMainAffix, List[SingleRelicMainAffix])
RelicSubAffixConfig = convert(RelicSubAffix, List[SingleRelicSubAffix])
