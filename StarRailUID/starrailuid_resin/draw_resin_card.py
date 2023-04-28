# import json
# import asyncio
# from typing import List
from pathlib import Path

from PIL import Image

# from PIL import ImageDraw
# from gsuid_core.logger import logger
# from gsuid_core.utils.api.mys.models import Expedition

# from ..utils.mys_api import mys_api
# from ..utils.api import get_sqla
# from ..utils.image.convert import convert_img
# from ..utils.image.image_tools import get_simple_bg
# from ..utils.map.name_covert import enName_to_avatarId
# from ..utils.resource.RESOURCE_PATH import PLAYER_PATH, CHAR_SIDE_PATH
# from ..utils.fonts.starrail_fonts import (
#     sr_font_20,
#     sr_font_26,
#     sr_font_32,
#     sr_font_60,
# )

TEXT_PATH = Path(__file__).parent / 'texture2D'

note_bg = Image.open(TEXT_PATH / 'note_bg.png')
note_travel_bg = Image.open(TEXT_PATH / 'note_travel_bg.png')

based_w = 500
based_h = 900
white_overlay = Image.new('RGBA', (based_w, based_h), (255, 251, 242, 225))

first_color = (29, 29, 29)
second_color = (98, 98, 98)
green_color = (15, 196, 35)
orange_color = (237, 115, 61)
red_color = (235, 61, 75)


# async def _draw_task_img(
#     img: Image.Image,
#     img_draw: ImageDraw.ImageDraw,
#     index: int,
#     char: Expedition,
# ):
#     char_en_name = char['avatar_side_icon'].split('_')[-1].split('.')[0]
#     avatar_id = await enName_to_avatarId(char_en_name)
#     char_pic = (
#         Image.open(CHAR_SIDE_PATH / f'{avatar_id}.png')
#         .convert('RGBA')
#         .resize((80, 80), Image.Resampling.LANCZOS)  # type: ignore
#     )
#     img.paste(char_pic, (22 + index * 90, 770), char_pic)
#     if char['status'] == 'Finished':
#         status_mark = '待收取'
#         status_color = red_color
#     else:
#         status_mark = '已派遣'
#         status_color = green_color
#     img_draw.text(
#         (65 + index * 90, 870),
#         status_mark,
#         font=sr_font_20,
#         fill=status_color,
#         anchor='mm',
#     )


async def get_resin_img(bot_id: str, user_id: str):
    pass
    # try:
    #     sqla = get_sqla(bot_id)
    #     uid_list: List = await sqla.get_bind_uid_list(user_id)
    #     logger.info('[每日信息]UID: {}'.format(uid_list))
    #     # 进行校验UID是否绑定CK
    #     useable_uid_list = []
    #     for uid in uid_list:
    #         status = await sqla.get_user_cookie(uid)
    #         if status is not None:
    #             useable_uid_list.append(uid)
    #     logger.info('[每日信息]可用UID: {}'.format(useable_uid_list))
    #     if len(useable_uid_list) == 0:
    #         return '请先绑定一个可用CK & UID再来查询哦~'
    #     # 开始绘图任务
    #     task = []
    #     img = Image.new(
    #         'RGBA', (based_w * len(useable_uid_list), based_h), (0, 0, 0, 0)
    #     )
    #     for uid_index, uid in enumerate(useable_uid_list):
    #         task.append(_draw_all_resin_img(img, uid, uid_index))
    #     await asyncio.gather(*task)
    #     res = await convert_img(img)
    #     logger.info('[查询每日信息]绘图已完成,等待发送!')
    # except TypeError:
    #     logger.exception('[查询每日信息]绘图失败!')
    #     res = '你绑定过的UID中可能存在过期CK~请重新绑定一下噢~'
    #
    # return res
