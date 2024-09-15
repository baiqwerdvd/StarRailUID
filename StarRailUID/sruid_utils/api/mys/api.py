# flake8: noqa
OLD_URL = "https://api-takumi.mihoyo.com"
OS_OLD_URL = "https://api-os-takumi.mihoyo.com"
NEW_URL = "https://api-takumi-record.mihoyo.com"
OS_URL = "https://sg-public-api.hoyolab.com"
OS_INFO_URL = "https://bbs-api-os.hoyolab.com"

STAR_RAIL_SIGN_INFO_URL = f"{OLD_URL}/event/luna/info"
STAR_RAIL_SIGN_INFO_URL_OS = f"{OS_URL}/event/luna/os/info"
STAR_RAIL_SIGN_LIST_URL = f"{OLD_URL}/event/luna/home"
STAR_RAIL_SIGN_LIST_URL_OS = f"{OS_URL}/event/luna/os/home"
STAR_RAIL_SIGN_EXTRA_INFO_URL = f"{OLD_URL}/event/luna/extra_info"
STAR_RAIL_SIGN_EXTRA_REWARD_URL = f"{OLD_URL}/event/luna/extra_reward"
STAR_RAIL_SIGN_URL = f"{OLD_URL}/event/luna/sign"
STAR_RAIL_SIGN_URL_OS = f"{OS_URL}/event/luna/os/sign"
STAR_RAIL_MONTH_INFO_URL = f"{OLD_URL}/event/srledger/month_info"  # 开拓阅历接口
STAR_RAIL_MONTH_DETAIL_URL = (
    f"{OLD_URL}/event/srledger/month_detail"  # 开拓阅历详情接口
)

STAR_RAIL_NOTE_URL = f"{NEW_URL}/game_record/app/hkrpg/api/note"  # 实时便签接口
STAR_RAIL_NOTE_URL_OS = f"{OS_INFO_URL}/game_record/hkrpg/api/note"  # OS实时便签接口
STAR_RAIL_INDEX_URL = f"{NEW_URL}/game_record/app/hkrpg/api/index"  # 角色橱窗接口
STAR_RAIL_INDEX_URL_OS = f"{OS_INFO_URL}/game_record/hkrpg/api/index"  # OS角色橱窗接口
STAR_RAIL_AVATAR_BASIC_URL = (
    f"{NEW_URL}/game_record/app/hkrpg/api/avatar/basic"  # 全部角色接口
)
STAR_RAIL_ROLE_BASIC_INFO_URL = (
    f"{NEW_URL}/game_record/app/hkrpg/api/role/basicInfo"  # 角色基础信息接口
)
STAR_RAIL_ROLE_BASIC_INFO_URL_OS = f"{OS_INFO_URL}/game_record/hkrpg/api/index"
STAR_RAIL_AVATAR_INFO_URL = (
    f"{NEW_URL}/game_record/app/hkrpg/api/avatar/info"  # 角色详细信息接口
)
STAR_RAIL_AVATAR_INFO_URL_OS = (
    f"{OS_INFO_URL}/game_record/hkrpg/api/avatar/info"  # OS角色详细信息接口
)

STAR_RAIL_AVATAR_LIST_URL = f"{OLD_URL}/event/rpgcalc/avatar/list"
STAR_RAIL_AVATAR_DETAIL_URL = f"{OLD_URL}/event/rpgcalc/avatar/detail"

CHALLENGE_INFO_URL = f"{NEW_URL}/game_record/app/hkrpg/api/challenge"  # 忘却之庭
CHALLENGE_INFO_URL_OS = f"{OS_INFO_URL}/game_record/hkrpg/api/challenge"  # OS忘却之庭
CHALLENGE_STORY_INFO_URL = (
    f"{NEW_URL}/game_record/app/hkrpg/api/challenge_story"  # 虚构叙事
)
CHALLENGE_BOSS_INFO_URL = (
    f"{NEW_URL}/game_record/app/hkrpg/api/challenge_boss"  # 末日幻影
)

ROGUE_INFO_URL = f"{NEW_URL}/game_record/app/hkrpg/api/rogue"  # 角色模拟宇宙信息接口
ROGUE_LOCUST_INFO_URL = (
    f"{NEW_URL}/game_record/app/hkrpg/api/rogue_locust"  # 角色寰宇蝗灾信息接口
)

STAR_RAIL_GACHA_LOG_URL = f"https://public-operation-hkrpg.mihoyo.com/common/gacha_record/api/getGachaLog"
STAR_RAIL_GACHA_LOG_URL_OS = f"{OS_OLD_URL}/common/gacha_record/api/getGachaLog"

GET_FP_URL = "https://public-data-api.mihoyo.com/device-fp/api/getFp"
GET_FP_URL_OS = "https://sg-public-data-api.hoyoverse.com/device-fp/api/getFp"
# CREATE_QRCODE = f'{OLD_URL}/event/bbs_sign_reward/gen_auth_code'

STAR_RAIL_WIDGRT_URL = f"{NEW_URL}/game_record/app/hkrpg/aapi/widget"

_API = locals()
