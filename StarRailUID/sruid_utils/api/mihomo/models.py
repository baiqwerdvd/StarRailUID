from __future__ import annotations

from msgspec import Struct, field


class MihomoData(Struct):
    detailInfo: PlayerDetailInfo


class Behavior(Struct):
    pointId: int
    level: int


class Equipment(Struct):
    level: int
    tid: int
    promotion: int | None = field(default=0)
    rank: int | None = field(default=0)


class Relic(Struct):
    subAffixList: list[SubAffix]
    tid: int
    mainAffixId: int
    type: int
    level: int | None = field(default=0)


class SubAffix(Struct):
    affixId: int
    cnt: int
    step: int | None = field(default=0)


class Avatar(Struct):
    skillTreeList: list[Behavior]
    avatarId: int
    level: int
    equipment: Equipment | None
    relicList: list[Relic]
    pos: int | None = field(default=0)
    rank: int | None = field(default=0)
    promotion: int | None = field(default=0)


class Challenge(Struct):
    scheduleMaxLevel: int
    MazeGroupIndex: int | None = None
    PreMazeGroupIndex: int | None = None


class PlayerSpaceInfo(Struct):
    challengeInfo: Challenge
    maxRogueChallengeScore: int
    equipmentCount: int
    avatarCount: int
    achievementCount: int


class PlayerDetailInfo(Struct):
    assistAvatarDetail: Avatar
    platform: str
    isDisplayAvatar: bool
    avatarDetailList: list[Avatar] | None
    uid: int
    friendCount: int
    worldLevel: int
    nickname: str
    level: int
    recordInfo: PlayerSpaceInfo | None
    headIcon: int
    signature: str | None = None
    Birthday: int | None = None
