################
# 签到相关 #
################
from typing import Any, List, TypedDict


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
