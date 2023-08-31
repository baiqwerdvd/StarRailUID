from __future__ import annotations

from typing import TypedDict, Union


class MihomoData(TypedDict):
    detailInfo: PlayerDetailInfo


class Behavior(TypedDict):
    pointId: int
    level: int


class Equipment(TypedDict):
    level: int
    tid: int
    promotion: Union[int, None]
    rank: Union[int, None]


class Relic(TypedDict):
    subAffixList: list[SubAffix]
    tid: int
    mainAffixId: int
    type: int


class SubAffix(TypedDict):
    affixId: int
    cnt: int
    step: int


class Avatar(TypedDict):
    skillTreeList: list[Behavior]
    rank: Union[int, None]
    pos: Union[int, None]
    avatarId: int
    level: int
    equipment: Union[Equipment, None]
    relicList: list[Relic]
    promotion: int


class Challenge(TypedDict):
    scheduleMaxLevel: int
    MazeGroupIndex: Union[int, None]
    PreMazeGroupIndex: Union[int, None]


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
    avatarDetailList: Union[list[Avatar], None]
    uid: int
    friendCount: int
    worldLevel: int
    nickname: str
    Birthday: Union[int, None]
    level: int
    recordInfo: Union[PlayerSpaceInfo, None]
    headIcon: int
    signature: Union[str, None]
