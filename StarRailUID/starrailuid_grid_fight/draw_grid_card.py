from pathlib import Path
from typing import Union

import msgspec
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.utils.error_reply import get_error
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_pic_with_ring
from PIL import Image, ImageDraw

from ..sruid_utils.api.mys.models import AbyssAvatar, AbyssPeakData
from ..utils.error_reply import prefix
from ..utils.fonts.starrail_fonts import (
    sr_font_22,
    sr_font_28,
    sr_font_30,
    sr_font_32,
    sr_font_34,
    sr_font_40,
    sr_font_42,
)
from ..utils.image.image_tools import _get_event_avatar, elements
from ..utils.mys_api import mys_api


async def draw_grid_img(
    ev: Event,
    uid: str,
):
    raw_grid_data = await mys_api.get_sr_grid_fight_info(uid)
    if isinstance(raw_grid_data, int):
        return get_error(raw_grid_data)

    # 获取查询者数据
    logger.debug(raw_grid_data)

    if not raw_grid_data.grid_fight_brief.has_played:
        return f"还没玩过呢~别查！"

    return "施工中"
