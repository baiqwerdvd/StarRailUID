from typing import Any, List, TypedDict


################
# 实时便签 #
################
class SingleExpedition(TypedDict):
    avatars: List[str]  # 头像Url
    status: str
    remaining_time: int
    name: str


class DailyNoteData(TypedDict):
    current_stamina: int
    max_stamina: int
    stamina_recover_time: int
    accepted_expedition_num: int
    total_expedition_num: int
    expeditions: List[SingleExpedition]


################
# 签到相关 #
################
class MysSign(TypedDict):
    code: str
    risk_code: int
    gt: str
    challenge: str
    success: int
    is_risk: bool


class SignInfo(TypedDict):
    total_sign_day: int
    today: str
    is_sign: bool
    is_sub: bool
    region: str
    sign_cnt_missed: int
    short_sign_day: int


class SignAward(TypedDict):
    icon: str
    name: str
    cnt: int


class SignExtraAward(TypedDict):
    has_extra_award: bool
    start_time: str
    end_time: str
    list: List[Any]  # TODO
    start_timestamp: str
    end_timestamp: str


class SignList(TypedDict):
    month: int
    awards: List[SignAward]
    biz: str
    resign: bool
    short_extra_award: SignExtraAward
