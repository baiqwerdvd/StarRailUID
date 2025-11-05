from typing import Any, Dict, List, Optional, Union

from msgspec import Struct


class AvatarDetailEquipment(Struct):
    item_id: str
    item_name: str
    item_url: str
    avatar_base_type: str
    rarity: str
    max_level: int
    cur_level: int
    target_level: int


class AvatarDetailSkill(Struct):
    point_id: str
    pre_point: str
    point_type: int
    anchor: str
    item_url: str
    max_level: int
    cur_level: int
    target_level: int
    progress: str
    min_level_limit: int


class AvatarDetailAvatar(Struct):
    item_id: str
    item_name: str
    icon_url: str
    damage_type: str
    rarity: str
    avatar_base_type: str
    max_level: int
    cur_level: int
    target_level: int
    vertical_icon_url: str


class AvatarDetail(Struct):
    avatar: AvatarDetailAvatar
    skills: List[AvatarDetailSkill]
    skills_other: List[AvatarDetailSkill]
    equipment: Union[AvatarDetailEquipment, None]
    is_login: bool


################
# 抽卡记录相关 #
################


class SingleGachaLog(Struct):
    uid: str
    gacha_id: str
    gacha_type: str
    item_id: str
    count: str
    time: str
    name: str
    lang: str
    item_type: str
    rank_type: str
    id: str


class GachaLog(Struct):
    page: str
    size: str
    list: List[SingleGachaLog]
    region: str
    region_time_zone: int


class RoleBasicInfo(Struct):
    avatar: str
    nickname: str
    region: str
    level: int


################
# 模拟宇宙相关 #
################


class RogueTime(Struct):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int


class RogueAvatar(Struct):
    id: int
    icon: str
    level: int
    rarity: int
    element: str
    rank: int


class RogueBaseType(Struct):
    id: int
    name: str
    cnt: int


class RogueBuffitems(Struct):
    id: int
    name: str
    is_evoluted: bool
    rank: int


class RogueMiracles(Struct):
    id: int
    name: str
    icon: str


class RogueBuffs(Struct):
    base_type: RogueBaseType
    items: List[RogueBuffitems]


class RogueRecordInfo(Struct):
    name: str
    finish_time: RogueTime
    score: int
    final_lineup: List[RogueAvatar]
    base_type_list: List[RogueBaseType]
    cached_avatars: List[RogueAvatar]
    buffs: List[RogueBuffs]
    miracles: List[RogueMiracles]
    difficulty: int
    progress: int
    detail_h: Union[int, None] = None
    start_h: Union[int, None] = None


class RogueBasic(Struct):
    id: int
    finish_cnt: int
    schedule_begin: RogueTime
    schedule_end: RogueTime


class RogueRecord(Struct):
    basic: RogueBasic
    records: List[RogueRecordInfo]


class RogueBasicInfo(Struct):
    unlocked_buff_num: int
    unlocked_miracle_num: int
    unlocked_skill_points: int


class LocustCntInfo(Struct):
    narrow: int
    miracle: int
    event: int


class LocustDestinyInfo(Struct):
    id: int
    desc: str
    level: int


class LocustBasicInfo(Struct):
    cnt: LocustCntInfo
    destiny: List[LocustDestinyInfo]


class RoleInfo(Struct):
    server: str
    nickname: str
    level: int


class LocustBlocks(Struct):
    block_id: int
    name: str
    num: int


class LocustFury(Struct):
    type: int
    point: str


class LocustRecordInfo(Struct):
    name: str
    finish_time: RogueTime
    final_lineup: List[RogueAvatar]
    base_type_list: List[RogueBaseType]
    cached_avatars: List[RogueAvatar]
    buffs: List[RogueBuffs]
    miracles: List[RogueMiracles]
    blocks: List[LocustBlocks]
    difficulty: int
    fury: LocustFury
    detail_h: Union[int, None] = None
    start_h: Union[int, None] = None

    # def __setitem__(self, key: str, value: Any) -> None:
    # self.__dict__[key] = value


class LocustRecord(Struct):
    records: List[LocustRecordInfo]


class RogueData(Struct):
    role: RoleInfo
    basic_info: RogueBasicInfo
    current_record: RogueRecord
    last_record: RogueRecord


class RogueLocustData(Struct):
    role: RoleInfo
    basic: LocustBasicInfo
    detail: LocustRecord


################
#   深渊相关   #
################


class AbyssTime(Struct):
    year: int
    month: int
    day: int
    hour: int
    minute: int


class AbyssAvatar(Struct):
    id: int
    level: int
    icon: str
    rarity: int
    element: str
    rank: int


class AbyssNodeDetail(Struct):
    challenge_time: Union[AbyssTime, None]
    avatars: List[AbyssAvatar]
    score: Optional[str] = None


class AbyssFloorDetail(Struct):
    name: str
    star_num: Union[int, str]
    node_1: AbyssNodeDetail
    node_2: AbyssNodeDetail
    round_num: Optional[int] = None
    is_fast: Optional[bool] = False


class AbyssData(Struct):
    schedule_id: int
    begin_time: AbyssTime
    end_time: AbyssTime
    star_num: int
    max_floor: str
    battle_num: int
    has_data: bool
    all_floor_detail: List[AbyssFloorDetail]
    max_floor_detail: Union[bool, None] = None


class AbyssStoryData(Struct):
    groups: Any
    star_num: int
    max_floor: str
    battle_num: int
    has_data: bool
    all_floor_detail: List[AbyssFloorDetail]
    max_floor_id: int


class AbyssBossData(Struct):
    groups: Any
    star_num: int
    max_floor: str
    battle_num: int
    has_data: bool
    all_floor_detail: List[AbyssFloorDetail]
    max_floor_id: int


class AbyssPeakMobRecord(Struct):
    maze_id: int
    has_challenge_record: bool
    round_num: int
    star_num: int
    is_fast: bool
    avatars: List[AbyssAvatar]
    challenge_time: Union[AbyssTime, None]


class AbyssPeakMobInfo(Struct):
    monster_name: str
    maze_id: int
    name: str
    monster_icon: str


class AbyssPeakBossInfo(Struct):
    name_mi18n: str
    icon: str
    maze_id: int
    hard_mode_name_mi18n: str


class AbyssPeakGroupInfo(Struct):
    name_mi18n: str
    theme_pic_path: str
    begin_time: AbyssTime
    end_time: AbyssTime
    status: str
    group_id: int
    game_version: str


class AbyssPeakBuff(Struct):
    desc_mi18n: str
    id: int
    name_mi18n: str
    icon: str


class AbyssPeakBossRecord(Struct):
    challenge_time: AbyssTime
    maze_id: int
    avatars: List[AbyssAvatar]
    hard_mode: bool
    round_num: int
    has_challenge_record: bool
    star_num: int
    challenge_peak_rank_icon_type: str
    challenge_peak_rank_icon: str
    buff: AbyssPeakBuff
    finish_color_medal: bool


class AbyssPeakRecord(Struct):
    mob_records: List[AbyssPeakMobRecord]
    boss_info: AbyssPeakBossInfo
    mob_infos: List[AbyssPeakMobInfo]
    has_challenge_record: bool
    battle_num: int
    boss_stars: int
    group: AbyssPeakGroupInfo
    mob_stars: int
    boss_record: Union[AbyssPeakBossRecord, None]


class AbyssPeakBestRecord(Struct):
    total_battle_num: int
    mob_stars: int
    boss_stars: int
    challenge_peak_rank_icon_type: str
    challenge_peak_rank_icon: str


class AbyssPeakData(Struct):
    challenge_peak_records: List[AbyssPeakRecord]
    has_more_boss_record: bool
    challenge_peak_best_record_brief: Union[AbyssPeakBestRecord, None]


################
# 每月札记相关 #
################


class DataText(Struct):
    type: str
    key: str
    mi18n_key: str


class DayData(Struct):
    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int


class GroupBy(Struct):
    action: str
    num: int
    percent: int
    action_name: str


class MonthData(Struct):
    current_hcoin: int
    current_rails_pass: int
    last_hcoin: int
    last_rails_pass: int
    hcoin_rate: int
    rails_rate: int
    group_by: List[GroupBy]


class MonthlyAward(Struct):
    uid: str
    region: str
    login_flag: bool
    optional_month: List[str]
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
class Expedition(Struct):
    avatars: List[str]  # 头像Url
    status: str
    remaining_time: int
    name: str


class DailyNoteData(Struct):
    current_stamina: int
    max_stamina: int
    stamina_recover_time: int
    accepted_expedition_num: int
    total_expedition_num: int
    expeditions: List[Expedition]


class WidgetStamina(Struct):
    current_stamina: int
    max_stamina: int
    stamina_recover_time: int
    accepted_expedition_num: int
    total_expedition_num: int
    expeditions: List[Expedition]
    current_train_score: int
    max_train_score: int
    current_rogue_score: int
    max_rogue_score: int
    has_signed: bool
    sign_url: str
    home_url: str
    note_url: str


################
# 签到相关 #
################
class MysSign(Struct):
    code: str
    risk_code: int
    gt: str
    challenge: str
    success: int
    is_risk: bool


class SignInfo(Struct):
    total_sign_day: int
    today: str
    is_sign: bool
    is_sub: bool
    region: str
    sign_cnt_missed: int
    short_sign_day: int


class SignAward(Struct):
    icon: str
    name: str
    cnt: int


class SignExtraAward(Struct):
    has_extra_award: bool
    start_time: str
    end_time: str
    list: List[Any]  # TODO
    start_timestamp: str
    end_timestamp: str


class SignList(Struct):
    month: int
    awards: List[SignAward]
    biz: str
    resign: bool
    short_extra_award: SignExtraAward


#####################
# 基础信息 角色信息 #
####################


class Stats(Struct):
    active_days: int
    avatar_num: int
    achievement_num: int
    chest_num: int
    abyss_process: str


class AvatarListItem(Struct):
    id: int
    level: int
    name: str
    element: str
    icon: str
    rarity: int
    rank: int
    is_chosen: bool


class RoleIndex(Struct):
    stats: Stats
    avatar_list: List[AvatarListItem]


################
# 角色详细信息 #
################


class Equip(Struct):
    id: int
    level: int
    rank: int
    name: str
    desc: str
    icon: str


class RelicsItem(Struct):
    id: int
    level: int
    pos: int
    name: str
    desc: str
    icon: str
    rarity: int


class RanksItem(Struct):
    id: int
    pos: int
    name: str
    icon: str
    desc: str
    is_unlocked: bool


class AvatarListItemDetail(Struct):
    id: int
    level: int
    name: str
    element: str
    icon: str
    rarity: int
    rank: int
    image: str
    equip: Union[Equip, None]
    relics: List[RelicsItem]
    ornaments: List
    ranks: List[RanksItem]


class AvatarInfo(Struct):
    avatar_list: List[AvatarListItemDetail]
    equip_wiki: Dict[str, str]
    relic_wiki: Dict
