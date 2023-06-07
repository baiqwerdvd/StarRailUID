from __future__ import annotations

from typing import List, Optional, TypedDict


class MihomoData(TypedDict):
    detailInfo: PlayerDetailInfo


class Behavior(TypedDict):
    pointId: int
    level: int


class Equipment(TypedDict):
    level: int
    tid: int
    promotion: Optional[int]
    rank: Optional[int]


class Relic(TypedDict):
    subAffixList: List[subAffixList]
    tid: int
    mainAffixId: int
    type: int


class Avatar(TypedDict):
    skillTreeList: List[Behavior]
    rank: Optional[int]
    pos: Optional[int]
    avatarId: int
    level: int
    equipment: Optional[Equipment]
    relicList: List[Relic]
    promotion: int


class Challenge(TypedDict):
    scheduleMaxLevel: int
    MazeGroupIndex: Optional[int]
    PreMazeGroupIndex: Optional[int]


class PlayerSpaceInfo(TypedDict):
    challengeInfo: Challenge
    maxRogueChallengeScore: int
    equipmentCount: int
    avatarCount: int
    achievementCount: int


class PlayerDetailInfo(TypedDict):
    assistAvatarDetail: Avatar
    platform: str
    isDisplayAvatar: bool
    avatarDetailList: Optional[List[Avatar]]
    uid: int
    friendCount: int
    worldLevel: int
    nickname: str
    Birthday: Optional[int]
    level: int
    recordInfo: Optional[PlayerSpaceInfo]
    headIcon: int
    signature: Optional[str]
