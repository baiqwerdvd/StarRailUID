from gsuid_core.logger import logger
from starrail_damage_cal.map import SR_MAP_PATH
from starrail_damage_cal.mihomo.requests import get_char_card_info
from starrail_damage_cal.model import MihomoCharacter
from starrail_damage_cal.to_data import api_to_dict, mys_to_dict

from ..starrailuid_config.sr_config import get_panel_source
from ..utils.mys_api import mys_api
from ..utils.resource.RESOURCE_PATH import PLAYER_PATH

PANEL_SOURCE_CONFIG_KEY = "PanelSource"
PANEL_SOURCE_HINT = (
    "全局面板数据源可选: auto(优先米游社, 失败回退 mihomo) / mihomo(仅 mihomo)\n"
    f"请在插件配置项 {PANEL_SOURCE_CONFIG_KEY} 中修改"
)


async def fetch_panel_data(
    uid: str,
) -> tuple[list[str], dict[str, MihomoCharacter], str]:
    """Fetch panel data with the configured source strategy."""
    if get_panel_source() != "mihomo":
        try:
            result = await mys_api.get_avatar_panel_info(uid)
            if not isinstance(result, int):
                nick_name, avatar_info = result
                avatar_list = _filter_supported_avatars(
                    avatar_info.avatar_list,
                    uid,
                    "米游社",
                    "id",
                )
                if not avatar_list:
                    logger.warning(f"[sr面板] UID{uid} 米游社面板中无可用角色, 回退至 mihomo")
                else:
                    char_id_list, chars = await mys_to_dict(
                        uid,
                        nick_name,
                        avatar_list,
                        save_path=PLAYER_PATH,
                    )
                    return char_id_list, chars, "mys"
            else:
                logger.warning(f"[sr面板] UID{uid} 米游社面板获取失败, 回退至 mihomo, code={result}")
        except Exception as exc:
            logger.warning(f"[sr面板] UID{uid} 米游社面板获取异常, 回退至 mihomo, error={exc}")

    mihomo_raw = await get_char_card_info(uid)
    mihomo_raw.detailInfo.avatarDetailList = _filter_supported_avatars(
        mihomo_raw.detailInfo.avatarDetailList,
        uid,
        "mihomo",
        "avatarId",
    )
    mihomo_raw.detailInfo.assistAvatarList = _filter_supported_avatars(
        mihomo_raw.detailInfo.assistAvatarList,
        uid,
        "mihomo",
        "avatarId",
    )
    if not mihomo_raw.detailInfo.avatarDetailList and not mihomo_raw.detailInfo.assistAvatarList:
        return [], {}, "mihomo"
    char_id_list, chars = await api_to_dict(uid, mihomo_raw=mihomo_raw, save_path=PLAYER_PATH)
    return char_id_list, chars, "mihomo"


def _filter_supported_avatars(avatars: object, uid: str, source: str, id_attr: str) -> list:
    if not avatars:
        return []

    supported = []
    skipped = []
    for avatar in avatars:
        avatar_id = getattr(avatar, id_attr, None)
        if str(avatar_id) in SR_MAP_PATH.avatarId2Name:
            supported.append(avatar)
        else:
            skipped.append(str(avatar_id))

    if skipped:
        skipped_ids = ", ".join(skipped)
        logger.warning(f"[sr面板] UID{uid} {source} 返回了未收录角色ID, 已跳过: {skipped_ids}")

    return supported
