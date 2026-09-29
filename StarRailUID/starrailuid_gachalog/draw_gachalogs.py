import asyncio
import json
from pathlib import Path

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_pic_with_ring, get_color_bg

from .gacha_stats import CHANGE_MAP as CHANGE_MAP, build_gacha_statistics
from ..utils.error_reply import prefix
from ..utils.fonts.starrail_fonts import (
    sr_font_14,
    sr_font_18,
    sr_font_20,
    sr_font_24,
    sr_font_28,
    sr_font_32,
    sr_font_40,
)
from ..utils.image.image_tools import _get_event_avatar
from ..utils.name_covert import name_to_avatar_id, name_to_weapon_id
from ..utils.resource.RESOURCE_PATH import CHAR_ICON_PATH, PLAYER_PATH, WEAPON_PATH

TEXT_PATH = Path(__file__).parent / "texture2d"
EMO_PATH = Path(__file__).parent / "texture2d" / "emo"

bg1_img = Image.open(TEXT_PATH / "bg1.png")
card_bg_img = (
    Image.open(TEXT_PATH / "char_bg.png").convert("RGBA").resize((160, 160)).crop((14, 0, 146, 160))
)

first_color = (29, 29, 29)
brown_color = (41, 25, 0)
red_color = (255, 66, 66)
green_color = (74, 189, 119)
white_color = (213, 213, 213)
whole_white_color = (255, 255, 255)

POOL_ORDER = ["角色跃迁", "光锥跃迁", "角色联动跃迁", "光锥联动跃迁", "群星跃迁", "始发跃迁"]
STANDARD_POOLS = {"群星跃迁", "始发跃迁"}
COL_W = 800
HEADER_H = 350
TITLE_H = 365
CARD_COLS = 5
CARD_ROW_H = 188
POOL_GAP = 20
FOOTER_H = 60
TWO_COL_MIN_FIVE = 41


async def _draw_card(
    img: Image.Image,
    xy_point: tuple[int, int],
    card_type: str,
    name: str,
    gacha_num: int,
    is_up: bool,
):
    card_img = Image.new("RGBA", (132, CARD_ROW_H))
    card_img.paste(card_bg_img, (0, 0), card_bg_img)
    card_img_draw = ImageDraw.Draw(card_img)
    if card_type == "角色":
        _id = await name_to_avatar_id(name)
        pic_path = CHAR_ICON_PATH / f"{_id}.png"
    else:
        _id = await name_to_weapon_id(name)
        pic_path = WEAPON_PATH / f"{_id}.png"
    if not pic_path.exists():
        logger.warning(f"[查询抽卡] {name} 图标缺失: {pic_path}")
        pic_path = CHAR_ICON_PATH / "999.png"
    if pic_path.exists():
        with Image.open(pic_path) as source:
            item_pic = source.convert("RGBA").resize((90, 90))
        card_img.paste(item_pic, (21, 23), item_pic)
    else:
        card_img_draw.text((66, 68), "暂无图标", brown_color, sr_font_18, "mm")
    if gacha_num >= 81:
        text_color = red_color
    elif gacha_num <= 55:
        text_color = green_color
    else:
        text_color = brown_color
    count_text = f"{gacha_num}抽" if gacha_num > 0 else "—"
    card_img_draw.rounded_rectangle((17, 118, 115, 148), radius=4, fill=(246, 231, 199))
    card_img_draw.text((66, 132), count_text, text_color, sr_font_24, "mm")
    name_font = sr_font_18 if card_img_draw.textlength(name, font=sr_font_18) <= 128 else sr_font_14
    display_name = name
    if card_img_draw.textlength(display_name, font=name_font) > 128:
        while card_img_draw.textlength(display_name + "…", font=name_font) > 128:
            display_name = display_name[:-1]
        display_name += "…"
    card_img_draw.rounded_rectangle((0, 153, 131, 183), radius=4, fill=(29, 29, 29, 230))
    card_img_draw.text((66, 168), display_name, whole_white_color, name_font, "mm")
    if is_up:
        card_img_draw.rounded_rectangle((86, 10, 130, 35), radius=6, fill=(255, 214, 130))
        card_img_draw.text((108, 23), "UP", brown_color, sr_font_18, "mm")
    img.paste(card_img, xy_point, card_img)


def _pool_block_height(total: int) -> int:
    rows = (total + CARD_COLS - 1) // CARD_COLS
    return TITLE_H + max(rows * CARD_ROW_H, 44) + POOL_GAP


def _pack_two_columns(pools: list[str], heights: dict[str, int]) -> tuple[list[str], list[str]]:
    """整池分列, 优先缩短画布, 其次平衡两列; 最高的卡池靠左。"""
    if len(pools) < 2:
        return pools, []
    tallest = max(pools, key=lambda name: heights[name])
    best_score = None
    best_columns = (pools, [])
    for mask in range(1, (1 << len(pools)) - 1):
        left = [name for index, name in enumerate(pools) if mask & (1 << index)]
        right = [name for name in pools if name not in left]
        left_h = sum(heights[name] for name in left)
        right_h = sum(heights[name] for name in right)
        score = (max(left_h, right_h), abs(left_h - right_h), tallest not in left, len(left))
        if best_score is None or score < best_score:
            best_score = score
            best_columns = (left, right)
    return best_columns


async def _compose_pool_title(pool_name: str, pool_data: dict, gacha_num: int) -> Image.Image:
    title = Image.open(TEXT_PATH / "bg2.png").convert("RGBA")
    title_draw = ImageDraw.Draw(title)
    # 覆盖素材中固定的“已 抽未出金”, 为联动池全名留出独立空间。
    title_draw.rectangle((90, 46, 697, 94), fill=(29, 29, 29))
    title_draw.text((110, 73), pool_name, whole_white_color, sr_font_32, "lm")
    title_draw.text((680, 73), f"已 {pool_data['remain']} 抽未出金", white_color, sr_font_24, "rm")

    if pool_name == "群星跃迁":
        average, thresholds = pool_data["avg"], [54, 61, 67, 73, 80]
    elif pool_name == "始发跃迁":
        average, thresholds = pool_data["avg"], [10, 20, 30, 40, 50]
    elif "光锥" in pool_name:
        average, thresholds = pool_data["avg_up"], [62, 75, 88, 99, 111]
    else:
        average, thresholds = pool_data["avg_up"], [74, 87, 99, 105, 120]
    level = await get_level_from_list(average, thresholds)
    emo_pic = (await random_emo_pic(level)).convert("RGBA").resize((175, 175))
    title.paste(emo_pic, (515, 130), emo_pic)

    avg = str(pool_data["avg"]) if pool_data["avg"] > 0 else "—"
    avg_up = (
        str(pool_data["avg_up"]) if pool_data["avg_up"] > 0 and pool_name not in STANDARD_POOLS else "—"
    )
    for x, value in ((143, avg), (280, avg_up), (413, str(gacha_num))):
        title_draw.text((x, 215), value, first_color, sr_font_40, "mm")
    title_draw.text((603, 310), f"五星 {pool_data['total']} 个", brown_color, sr_font_20, "mm")
    time_range = pool_data["time_range"] or "暂无时间记录"
    title_draw.text((78, 340), time_range, brown_color, sr_font_20, "lm")
    return title


async def random_emo_pic(level: int) -> Image.Image:
    emo_fold = EMO_PATH / f"3000{level}.png"
    return Image.open(emo_fold)


async def get_level_from_list(ast: int, lst: list) -> int:
    if ast == 0:
        return 3

    for num_index, num in enumerate(lst):
        if ast <= num:
            level = num_index + 1
            break
    else:
        level = 6
    return level


async def draw_gachalogs_img(uid: str, ev: Event) -> bytes | str:
    path = PLAYER_PATH / str(uid) / "gacha_logs.json"
    wx_path = PLAYER_PATH / str(uid) / "gacha_logs_wx.json"
    if not path.exists() and not wx_path.exists():
        return f"你还没有跃迁数据噢~\n请使用命令`{prefix}刷新抽卡记录`更新跃迁数据~"

    gacha_data: dict[str, str | int | dict[str, list[dict[str, str | int | bool]]]] = {}
    if path.exists():
        with Path.open(path, encoding="UTF-8") as f:
            loaded_data = json.load(f)
            if isinstance(loaded_data, dict):
                gacha_data = loaded_data

    wx_data: dict[str, str | int | dict[str, int] | dict[str, list[dict[str, str | int | bool]]]] = {}
    if wx_path.exists():
        with Path.open(wx_path, encoding="UTF-8") as f:
            loaded_wx = json.load(f)
            if isinstance(loaded_wx, dict):
                wx_data = loaded_wx

    if not gacha_data and not wx_data:
        return f"你还没有跃迁数据噢~\n请使用命令`{prefix}刷新抽卡记录`更新跃迁数据~"

    total_data, pool_counts = build_gacha_statistics(gacha_data, wx_data)

    # 有垫抽但尚未出金的卡池也需要展示。
    pools = [
        name
        for name in POOL_ORDER
        if total_data[name]["total"]
        or total_data[name]["remain"]
        or total_data[name]["time_range"]
        or pool_counts[name]
    ]
    heights = {name: _pool_block_height(total_data[name]["total"]) for name in pools}
    total_five = sum(total_data[name]["total"] for name in pools)
    if total_five >= TWO_COL_MIN_FIVE and len(pools) > 1:
        left, right = _pack_two_columns(pools, heights)
        columns = [(left, 0), (right, COL_W)]
    else:
        columns = [(pools, 0)]
    canvas_w = COL_W * len(columns)
    content_h = max(sum(heights[name] for name in names) for names, _ in columns)
    img = await get_color_bg(canvas_w, HEADER_H + max(content_h, 120) + FOOTER_H)

    char_pic = await _get_event_avatar(ev)
    char_pic = await draw_pic_with_ring(char_pic, 206, None, False)
    gacha_title = bg1_img.copy()
    gacha_title.paste(char_pic, (297, 81), char_pic)
    header_x = (canvas_w - COL_W) // 2
    img.paste(gacha_title, (header_x, 0), gacha_title)
    img_draw = ImageDraw.Draw(img)
    img_draw.text((canvas_w // 2, 345), f"UID {uid}", white_color, sr_font_28, "mm")

    for names, col_x in columns:
        y = HEADER_H
        for pool_name in names:
            pool_data = total_data[pool_name]
            title = await _compose_pool_title(pool_name, pool_data, pool_counts[pool_name])
            img.paste(title, (col_x, y), title)
            tasks = []
            for index, item in enumerate(reversed(pool_data["list"])):
                point = (
                    col_x + 60 + index % CARD_COLS * 136,
                    y + TITLE_H + index // CARD_COLS * CARD_ROW_H,
                )
                tasks.append(
                    _draw_card(
                        img,
                        point,
                        item["item_type"],
                        item["name"],
                        item["gacha_num"],
                        item["is_up"] and pool_name not in STANDARD_POOLS,
                    )
                )
            if tasks:
                await asyncio.gather(*tasks)
            else:
                img_draw.text(
                    (col_x + COL_W // 2, y + TITLE_H + 20),
                    "尚未获得五星",
                    white_color,
                    sr_font_20,
                    "mm",
                    stroke_width=1,
                    stroke_fill=first_color,
                )
            y += heights[pool_name]

    if not pools:
        img_draw.text(
            (canvas_w // 2, HEADER_H + 75),
            "暂无可展示的跃迁记录",
            white_color,
            sr_font_24,
            "mm",
            stroke_width=1,
            stroke_fill=first_color,
        )
    img_draw.text(
        (canvas_w // 2, img.height - 30),
        "StarRailUID · 跃迁记录 · 最新记录在前",
        white_color,
        sr_font_18,
        "mm",
        stroke_width=1,
        stroke_fill=first_color,
    )
    res = await convert_img(img)
    logger.info("[查询抽卡]绘图已完成,等待发送!")
    return res
