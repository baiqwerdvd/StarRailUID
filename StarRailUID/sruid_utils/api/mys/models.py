from typing import Any, List, TypedDict

################
# 每月札记相关 #
################


class DataText(TypedDict):
    type: str
    key: str
    mi18n_key: str


class DayData(TypedDict):
    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int


class GroupBy(TypedDict):
    action: str
    num: int
    percent: int
    action_name: str


class MonthData(TypedDict):
    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int
    hcoin_rate: int
    rails_rate: int
    group_by: List[GroupBy]


class MonthlyAward(TypedDict):
    uid: str
    region: str
    login_flag: bool
    optional_month: List[int]
    month: str
    data_month: str
    month_data: MonthData
    day_data: DayData
    version: str
    start_month: str
    data_text: DataText


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
