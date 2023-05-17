from __future__ import annotations

from typing import List, Optional, TypedDict


class MihomoData(TypedDict):
    PlayerDetailInfo: PlayerDetailInfo


class Behavior(TypedDict):
    BehaviorID: int
    Level: int


class Equipment(TypedDict):
    Level: int
    ID: int
    Promotion: Optional[int]
    Rank: Optional[int]


class Relic(TypedDict):
    RelicSubAffix: List[RelicSubAffix]
    ID: int
    MainAffixID: int
    Type: int


class Avatar(TypedDict):
    BehaviorList: List[Behavior]
    Rank: Optional[int]
    Pos: Optional[int]
    AvatarID: int
    Level: int
    EquipmentID: Optional[Equipment]
    RelicList: List[Relic]
    Promotion: int


class Challenge(TypedDict):
    PreMazeGroupIndex: int
    MazeGroupIndex: Optional[int]
    PreMazeGroupIndex: Optional[int]


class PlayerSpaceInfo(TypedDict):
    ChallengeData: Challenge
    PassAreaProgress: int
    LightConeCount: int
    AvatarCount: int
    AchievementCount: int


class PlayerDetailInfo(TypedDict):
    AssistAvatar: Avatar
    IsDisplayAvatarList: bool
    DisplayAvatarList: Optional[List[Avatar]]
    UID: int
    CurFriendCount: int
    WorldLevel: int
    NickName: str
    Birthday: Optional[int]
    Level: int
    PlayerSpaceInfo: Optional[PlayerSpaceInfo]
    HeadIconID: int
    Signature: Optional[str]
