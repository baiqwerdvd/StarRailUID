# flake8: noqa
OLD_URL = "https://api-takumi.mihoyo.com"

STAR_RAIL_SIGN_INFO_URL = f'{OLD_URL}/event/luna/info'
STAR_RAIL_SIGN_LIST_URL = f'{OLD_URL}/event/luna/home'
STAR_RAIL_SIGN_EXTRA_INFO_URL = f'{OLD_URL}/event/luna/extra_info'
STAR_RAIL_SIGN_EXTRA_REWARD_URL = f'{OLD_URL}/event/luna/extra_reward'
STAR_RAIL_SIGN_URL = f'{OLD_URL}/event/luna/sign'
STAR_RAIL_MONTH_INFO_URL = f'{OLD_URL}/event/srledger/month_info'  # 开拓阅历接口

STAR_RAIL_NOTE_URL = f'{OLD_URL}/game_record/app/hkrpg/api/note'  # 实时便签接口
STAR_RAIL_INDEX_URL = f'{OLD_URL}/game_record/app/hkrpg/api/index'  # 角色橱窗接口
STAR_RAIL_AVATAR_BASIC_URL = (
    f'{OLD_URL}/game_record/app/hkrpg/api/avatar/basic'  # 全部角色接口
)
STAR_RAIL_ROLE_BASIC_INFO_URL = (
    f'{OLD_URL}/game_record/app/hkrpg/api/role/basicInfo'  # 角色基础信息接口
)


# CREATE_QRCODE = f'{OLD_URL}/event/bbs_sign_reward/gen_auth_code'

_API = locals()
