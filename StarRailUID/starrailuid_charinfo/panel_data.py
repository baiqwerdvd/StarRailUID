from gsuid_core.logger import logger
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
                char_id_list, chars = await mys_to_dict(
                    uid,
                    nick_name,
                    avatar_info.avatar_list,
                    save_path=PLAYER_PATH,
                )
                return char_id_list, chars, "mys"
            logger.warning(f"[sr面板] UID{uid} 米游社面板获取失败, 回退至 mihomo, code={result}")
        except Exception as exc:
            logger.warning(f"[sr面板] UID{uid} 米游社面板获取异常, 回退至 mihomo, error={exc}")

    char_id_list, chars = await api_to_dict(uid, save_path=PLAYER_PATH)
    return char_id_list, chars, "mihomo"
