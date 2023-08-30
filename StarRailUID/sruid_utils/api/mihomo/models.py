from __future__ import annotations

from typing import TypedDict


class MihomoData(TypedDict):
    detailInfo: PlayerDetailInfo


class Behavior(TypedDict):
    pointId: int
    level: int


class Equipment(TypedDict):
    level: int
    tid: int
    promotion: int | None
    rank: int | None


class Relic(TypedDict):
    subAffixList: list[SubAffix]
    tid: int
    mainAffixId: int
    type: int


class SubAffix(TypedDict):
    affixID: int
    cnt: int
    step: int


class Avatar(TypedDict):
    skillTreeList: list[Behavior]
    rank: int | None
    pos: int | None
    avatarId: int
    level: int
    equipment: Equipment | None
    relicList: list[Relic]
    promotion: int


class Challenge(TypedDict):
    scheduleMaxLevel: int
    MazeGroupIndex: int | None
    PreMazeGroupIndex: int | None


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
    avatarDetailList: list[Avatar] | None
    uid: int
    friendCount: int
    worldLevel: int
    nickname: str
    Birthday: int | None
    level: int
    recordInfo: PlayerSpaceInfo | None
    headIcon: int
    signature: str | None
