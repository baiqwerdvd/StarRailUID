from typing import List, Union

from msgspec import Struct, field


class Behavior(Struct):
    pointId: int
    level: int


class Equipment(Struct):
    level: Union[int, None] = field(default=0)
    tid: Union[int, None] = None
    promotion: Union[int, None] = field(default=0)
    rank: Union[int, None] = field(default=0)


class SubAffix(Struct):
    affixId: int
    cnt: int
    step: Union[int, None] = field(default=0)


class Relic(Struct):
    tid: int
    mainAffixId: int
    type: int
    subAffixList: Union[List[SubAffix], None] = field(default=[])
    level: Union[int, None] = field(default=0)


class Avatar(Struct):
    skillTreeList: List[Behavior]
    avatarId: int
    level: int
    equipment: Union[Equipment, None] = None
    relicList: Union[List[Relic], None] = field(default=[])
    pos: Union[int, None] = field(default=0)
    rank: Union[int, None] = field(default=0)
    promotion: Union[int, None] = field(default=0)


class Challenge(Struct):
    scheduleMaxLevel: Union[int, None] = None
    MazeGroupIndex: Union[int, None] = None
    PreMazeGroupIndex: Union[int, None] = None


class PlayerSpaceInfo(Struct):
    maxRogueChallengeScore: int
    equipmentCount: int
    avatarCount: int
    achievementCount: int
    challengeInfo: Union[Challenge, None] = None


class PlayerDetailInfo(Struct):
    assistAvatarDetail: Avatar
    platform: str
    isDisplayAvatar: bool
    avatarDetailList: Union[List[Avatar], None]
    uid: int
    friendCount: int
    worldLevel: int
    nickname: str
    level: int
    recordInfo: Union[PlayerSpaceInfo, None]
    headIcon: int
    signature: Union[str, None] = None
    Birthday: Union[int, None] = None


class MihomoData(Struct):
    detailInfo: PlayerDetailInfo
