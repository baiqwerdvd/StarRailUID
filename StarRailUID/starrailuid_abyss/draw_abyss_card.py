from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw
from gsuid_core.models import Event
from gsuid_core.logger import logger
from gsuid_core.utils.error_reply import get_error
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_pic_with_ring

from ..utils.mys_api import mys_api
from ..utils.error_reply import prefix
from ..sruid_utils.api.mys.models import AbyssAvatar
from ..utils.resource.get_pic_from import get_roleinfo_icon
from ..utils.image.image_tools import elements, _get_event_avatar
from ..utils.fonts.starrail_fonts import (
    sr_font_22,
    sr_font_28,
    sr_font_30,
    sr_font_34,
    sr_font_42,
)

TEXT_PATH = Path(__file__).parent / "texture2D"
white_color = (255, 255, 255)
gray_color = (175, 175, 175)
img_bg = Image.open(TEXT_PATH / "bg.jpg")
level_cover = Image.open(TEXT_PATH / "level_cover.png").convert("RGBA")
char_bg_4 = Image.open(TEXT_PATH / "char4_bg.png").convert("RGBA")
char_bg_5 = Image.open(TEXT_PATH / "char5_bg.png").convert("RGBA")
rank_bg = Image.open(TEXT_PATH / "rank_bg.png").convert("RGBA")
star_yes = Image.open(TEXT_PATH / "star.png").convert("RGBA")
star_gray = Image.open(TEXT_PATH / "star_gray.png").convert("RGBA")


async def get_abyss_star_pic(star: int) -> Image.Image:
    return Image.open(TEXT_PATH / f"star{star}.png")


async def _draw_abyss_card(
    char: AbyssAvatar,
    floor_pic: Image.Image,
    index_char: int,
    index_part: int,
):
    char_bg = (char_bg_4 if char.rarity == 4 else char_bg_5).copy()
    char_icon = (await get_roleinfo_icon(char.icon)).resize((150, 170))
    element_icon = elements[char.element]
    char_bg.paste(char_icon, (24, 16), mask=char_icon)
    char_bg.paste(level_cover, (0, 0), mask=level_cover)
    char_bg.paste(element_icon, (35, 25), mask=element_icon)
    char_card_draw = ImageDraw.Draw(char_bg)
    if char.rank > 0:
        char_bg.paste(rank_bg, (150, 16), mask=rank_bg)
        char_card_draw.text(
            (162, 31),
            f"{char.rank}",
            font=sr_font_22,
            fill=white_color,
            anchor="mm",
        )
    char_card_draw.text(
        (100, 165),
        f"等级 {char.level}",
        font=sr_font_22,
        fill=white_color,
        anchor="mm",
    )
    floor_pic.paste(
        char_bg,
        (75 + 185 * index_char, 130 + index_part * 219),
        char_bg,
    )


async def _draw_floor_card(
    level_star: Union[int, str],
    floor_pic: Image.Image,
    img: Image.Image,
    index_floor: int,
    floor_name: str,
    round_num: Union[int, None],
):
    for index_num in [0, 1, 2]:
        star_num = index_num + 1
        if star_num <= int(level_star):
            star_pic = star_yes.copy()
        else:
            star_pic = star_gray.copy()
        floor_pic.paste(star_pic, (103 + index_num * 50, 25), star_pic)
    floor_pic_draw = ImageDraw.Draw(floor_pic)
    floor_pic_draw.text(
        (450, 60),
        floor_name,
        font=sr_font_42,
        fill=white_color,
        anchor="mm",
    )
    floor_pic_draw.text(
        (802, 60),
        f"使用轮: {round_num}",
        font=sr_font_28,
        fill=gray_color,
        anchor="rm",
    )
    img.paste(floor_pic, (0, 657 + index_floor * 570), floor_pic)


async def draw_abyss_img(
    ev: Event,
    uid: str,
    schedule_type: str = "1",
) -> Union[bytes, str]:
    raw_abyss_data = await mys_api.get_abyss_info(uid, schedule_type)

    if isinstance(raw_abyss_data, int):
        return get_error(raw_abyss_data)

    # 获取查询者数据
    if raw_abyss_data.max_floor == "":
        return f"你还没有挑战本期深渊!\n可以使用[{prefix}上期深渊]命令查询上期~"
    # 过滤掉 is_fast (快速通关) 为 True 的项
    floor_detail = [
        detail
        for detail in raw_abyss_data.all_floor_detail
        if not detail.is_fast
    ]
    floor_num = len(floor_detail)

    # 获取背景图片各项参数
    based_w = 900
    based_h = 657 + 570 * floor_num
    img = img_bg.copy()
    img = img.crop((0, 0, based_w, based_h))
    abyss_title = Image.open(TEXT_PATH / "head.png")
    img.paste(abyss_title, (0, 0), abyss_title)

    # 获取头像
    char_pic = await _get_event_avatar(ev)
    char_pic = await draw_pic_with_ring(char_pic, 250, None, False)

    img.paste(char_pic, (325, 132), char_pic)

    # 绘制抬头
    img_draw = ImageDraw.Draw(img)
    img_draw.text((450, 442), f"UID {uid}", white_color, sr_font_28, "mm")

    # 总体数据
    abyss_data = Image.open(TEXT_PATH / "data.png")
    img.paste(abyss_data, (0, 500), abyss_data)

    # 最深抵达
    img_draw.text(
        (220, 565),
        f"{raw_abyss_data.max_floor}",
        white_color,
        sr_font_34,
        "lm",
    )
    # 挑战次数
    img_draw.text(
        (220, 612),
        f"{raw_abyss_data.battle_num}",
        white_color,
        sr_font_34,
        "lm",
    )

    star_num_pic = Image.open(TEXT_PATH / "star.png")
    img.paste(star_num_pic, (615, 557), star_num_pic)

    img_draw.text(
        (695, 590),
        f"{raw_abyss_data.star_num}/36",
        white_color,
        sr_font_42,
        "lm",
    )

    for index_floor, level in enumerate(raw_abyss_data.all_floor_detail):
        floor_pic = Image.open(TEXT_PATH / "floor_bg.png")
        level_star = level.star_num
        floor_name = level.name
        round_num = level.round_num
        node_1 = level.node_1
        node_2 = level.node_2
        for index_part in [0, 1]:
            node_num = index_part + 1
            if node_num == 1:
                time_array = node_1.challenge_time
            else:
                time_array = node_2.challenge_time
            assert time_array is not None
            time_str = f"{time_array.year}-{time_array.month}"
            time_str = f"{time_str}-{time_array.day}"
            time_str = f"{time_str} {time_array.hour}:{time_array.minute}:00"
            floor_pic_draw = ImageDraw.Draw(floor_pic)
            floor_pic_draw.text(
                (112, 120 + index_part * 219),
                f"节点{node_num}",
                white_color,
                sr_font_30,
                "lm",
            )
            floor_pic_draw.text(
                (201, 120 + index_part * 219),
                f"{time_str}",
                gray_color,
                sr_font_22,
                "lm",
            )
            if node_num == 1:
                avatars_array = node_1
            else:
                avatars_array = node_2

            for index_char, char in enumerate(avatars_array.avatars):
                await _draw_abyss_card(
                    char,
                    floor_pic,
                    index_char,
                    index_part,
                )
        await _draw_floor_card(
            level_star,
            floor_pic,
            img,
            index_floor,
            floor_name,
            round_num,
        )

    res = await convert_img(img)
    logger.info("[查询深渊信息]绘图已完成,等待发送!")
    return res
