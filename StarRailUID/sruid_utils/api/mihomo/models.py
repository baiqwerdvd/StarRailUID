from typing import List, Union, Any

from msgspec import Struct, field


# 头像
class Avatar(Struct):
    id: str
    name: str
    icon: str


# 基本信息
class PlayerInfo(Struct):
    uid: str
    nickname: str
    level: int
    world_level: int
    friend_count: int
    avatar: Avatar
    signature: Union[str, None] = None


# 属性
class Attribute(Struct):
    field: str
    name: str
    icon: str
    value: float
    display: str
    percent: bool


# 属性1
class Properties(Attribute):
    percent: bool


# 元素
class Element(Struct):
    id: str
    name: str
    icon: str
    color: str


# 命途
class Path(Struct):
    id: str
    name: str
    icon: str


# 主词条
class MainAffix(Struct):
    type: str
    field: str
    name: str
    icon: str
    value: float
    display: str


# 副词条
class SubAffix(MainAffix):
    count: int
    step: int

    # 战技


class Skill(Struct):
    id: str
    name: str
    level: int
    max_level: int
    type: str
    type_text: str
    effect: str
    effect_text: str
    simple_desc: str
    desc: str
    icon: str


# 光锥
class LightCone(Struct):
    id: str
    name: str
    rarity: int
    rank: int
    level: int
    promotion: int
    icon: str
    preview: str
    portrait: str
    path: Path
    attributes: List[Attribute]
    properties: List[Properties]


# 遗器
class Relic(Struct):
    id: str
    type: int
    name: str
    set_id: str
    set_name: str
    rarity: int
    level: int
    icon: str
    main_affix: MainAffix
    sub_affix: List[SubAffix]


# 角色信息
class Character(Struct):
    id: str
    name: str
    rank: int
    rarity: int
    level: int
    promotion: int
    icon: str
    preview: str
    portrait: str
    rank_icons: List[str]
    element: Element
    skills: List[Skill]
    light_cone: LightCone
    relics: List[Relic]
    attributes: List[Attribute]
    additions: List[Attribute]


class MihomoData(Struct):
    player: PlayerInfo
    characters: List[Character]
