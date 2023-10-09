from typing import Dict, List, Union

from msgspec import Struct


class HakushHsrCharacterInfoVoiceline(Struct):
    VoiceID: int
    VoiceTitle: str
    VoiceM: str
    IsBattleVoice: bool
    UnlockDesc: Union[str, None] = None


class HakushHsrCharacterInfo(Struct):
    Camp: str
    VA: Dict[str, str]
    Stories: Dict[str, str]
    Voicelines: List[HakushHsrCharacterInfoVoiceline]


class HakushHsrCharacterRank(Struct):
    Id: int
    Name: str
    Desc: str
    ParamList: List[float]


class HakushHsrCharacterSkillLevel(Struct):
    Level: int
    ParamList: List[float]


class HakushHsrCharacterSkill(Struct):
    Name: str
    Desc: str
    Type: Union[str, None]
    Tag: str
    SPBase: Union[float, None]
    ShowStanceList: List[float]
    SkillComboValueDelta: Union[float, None]
    Level: Dict[str, HakushHsrCharacterSkillLevel]


class HakushHsrMaterial(Struct):
    ItemID: int
    ItemNum: int


class HakushHsrCharacterStatusAdd(Struct):
    PropertyType: str
    Value: float


class HakushHsrCharacterSkillTree(Struct):
    Anchor: str
    DefaultUnlock: bool
    Icon: str
    LevelUpSkillID: List[int]
    MaterialList: List[Union[HakushHsrMaterial, None]]
    MaxLevel: int
    ParamList: List[float]
    PointID: int
    PointName: str
    PointDesc: str
    PointTriggerKey: int
    PointType: int
    PrePoint: List[int]
    StatusAddList: List[Union[HakushHsrCharacterStatusAdd, None]]
    AvatarPromotionLimit: Union[int, None] = None
    AvatarLevelLimit: Union[int, None] = None


class HakushHsrCharacterStats(Struct):
    AttackBase: float
    AttackAdd: float
    DefenceBase: float
    DefenceAdd: float
    HPBase: float
    HPAdd: float
    SpeedBase: float
    CriticalChance: float
    CriticalDamage: float
    BaseAggro: float
    Cost: List[Union[HakushHsrMaterial, None]]


class HakushHsrCharacterRelicProperty(Struct):
    PropertyType: str
    RelicType: str


class HakushHsrCharacterRelic(Struct):
    AvatarID: int
    PropertyList: List[HakushHsrCharacterRelicProperty]
    Set2IDList: List[int]
    Set4IDList: List[int]


class HakushHsrCharacter(Struct):
    Name: str
    Desc: str
    CharaInfo: HakushHsrCharacterInfo
    Rarity: str
    AvatarVOTag: str
    SPNeed: float
    BaseType: str
    DamageType: str
    Ranks: Dict[str, HakushHsrCharacterRank]
    Skills: Dict[str, HakushHsrCharacterSkill]
    SkillTrees: Dict[str, Dict[str, HakushHsrCharacterSkillTree]]
    Stats: Dict[str, HakushHsrCharacterStats]
    Relics: HakushHsrCharacterRelic


class LightconeRefinementLevel(Struct):
    ParamList: List[float]


class HakushHsrLightconeRefinement(Struct):
    Desc: str
    Level: Dict[str, LightconeRefinementLevel]
    Name: str


class HakushHsrLightconeStat(Struct):
    BaseAttack: float
    BaseAttackAdd: float
    BaseDefence: float
    BaseDefenceAdd: float
    BaseHP: float
    BaseHPAdd: float
    EquipmentID: int
    MaxLevel: int
    PromotionCostList: List[HakushHsrMaterial]
    PlayerLevelRequire: Union[int, None] = None
    WorldLevelRequire: Union[int, None] = None


class HakushHsrLightcone(Struct):
    Name: str
    Desc: str
    Rarity: str
    BaseType: str
    Refinements: HakushHsrLightconeRefinement
    Stats: List[HakushHsrLightconeStat]


class HakushHsrCharacterIndex(Struct):
    icon: str
    rank: str
    baseType: str
    damageType: str
    en: str
    desc: str
    kr: str
    cn: str
    jp: str


class HakushHsrLightconeIndex(Struct):
    rank: str
    baseType: str
    en: str
    desc: str
    kr: str
    cn: str
    jp: str
