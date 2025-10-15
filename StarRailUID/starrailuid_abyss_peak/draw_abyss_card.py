from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.utils.error_reply import get_error
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_pic_with_ring

from ..sruid_utils.api.mys.models import AbyssAvatar
from ..utils.error_reply import prefix
from ..utils.fonts.starrail_fonts import (
    sr_font_22,
    sr_font_28,
    sr_font_30,
    sr_font_34,
    sr_font_42,
)
from ..utils.image.image_tools import _get_event_avatar, elements
from ..utils.mys_api import mys_api
from ..utils.resource.get_pic_from import get_roleinfo_icon



async def draw_abyss_img(
    ev: Event,
    uid: str,
    schedule_type: str = "1",
) -> Union[bytes, str]:
    raw_abyss_data = await mys_api.get_abyss_peak_info(uid, schedule_type)
    if isinstance(raw_abyss_data, int):
        return get_error(raw_abyss_data)

    # 获取查询者数据
    logger.debug(raw_abyss_data)
    if not raw_abyss_data.has_more_boss_record:
        return f"你还没有挑战本期异相仲裁!\n可以使用[{prefix}上期异相仲裁]命令查询上期~"
    
    logger.info("[查询异相仲裁信息]绘图已完成,等待发送!")
    return "功能开发中"