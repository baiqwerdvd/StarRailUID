import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.utils.image.convert import convert_img

from ..utils.error_reply import get_error
from ..utils.fonts.starrail_fonts import (
    sr_font_20,
    sr_font_22,
    sr_font_28,
    sr_font_30,
    sr_font_34,
    sr_font_42,
)
from ..utils.mys_api import mys_api
from ..utils.resource.get_pic_from import get_roleinfo_icon

TEXT_PATH = Path(__file__).parent / "texture2D"
BACKGROUND = Image.open(TEXT_PATH / "bg.jpg")

WHITE = (242, 245, 252)
GRAY = (172, 184, 203)
GOLD = (243, 214, 148)
CYAN = (107, 207, 239)
PANEL = (14, 25, 52, 205)
PANEL_BORDER = (72, 93, 129, 220)


def _value(data: Any, *path: str, default: Any = "-") -> Any:
    current = data
    for key in path:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


def _records(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    result = _value(data, key, "records", default=[])
    return result if isinstance(result, list) else []


def _format_time(value: Any) -> str:
    if not isinstance(value, dict):
        return "-"
    date = "-".join(
        str(value.get(key, 0)).zfill(2) if key != "year" else str(value.get(key, 0))
        for key in ("year", "month", "day")
    )
    time = ":".join(str(value.get(key, 0)).zfill(2) for key in ("hour", "minute"))
    return f"{date} {time}"


def _base_image(height: int) -> Image.Image:
    img = Image.new("RGB", (900, height), (9, 16, 38))
    for top in range(0, height, BACKGROUND.height):
        crop_height = min(BACKGROUND.height, height - top)
        img.paste(BACKGROUND.crop((0, 0, 900, crop_height)), (0, top))
    return img


def _panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=14, fill=PANEL, outline=PANEL_BORDER, width=2)


def _stat(
    draw: ImageDraw.ImageDraw,
    left: int,
    value: str,
    label: str,
) -> None:
    _panel(draw, (left, 128, left + 250, 232))
    draw.text((left + 125, 164), value, font=sr_font_34, fill=GOLD, anchor="mm")
    draw.text((left + 125, 207), label, font=sr_font_20, fill=GRAY, anchor="mm")


async def _draw_lineup(
    img: Image.Image,
    lineup: list[dict[str, Any]],
    top: int,
) -> None:
    draw = ImageDraw.Draw(img)
    for index, avatar in enumerate(lineup[:4]):
        left = 75 + index * 190
        _panel(draw, (left, top, left + 165, top + 188))
        icon_url = avatar.get("icon")
        if icon_url:
            try:
                icon = (await get_roleinfo_icon(icon_url)).resize((140, 140))
                img.paste(icon, (left + 12, top + 8), icon)
            except Exception as exc:
                logger.warning(f"[差分宇宙] 角色头像读取失败: {exc}")
        draw.text(
            (left + 82, top + 157),
            f"等级 {avatar.get('level', '-')}",
            font=sr_font_20,
            fill=WHITE,
            anchor="mm",
        )
        draw.text(
            (left + 143, top + 20),
            f"{avatar.get('rank', 0)}魂",
            font=sr_font_20,
            fill=GOLD,
            anchor="rm",
        )


def _draw_item_list(
    draw: ImageDraw.ImageDraw,
    title: str,
    items: list[Any],
    top: int,
) -> int:
    _panel(draw, (52, top, 848, top + 70 + max(1, math.ceil(len(items[:12]) / 3)) * 40))
    draw.text((78, top + 36), title, font=sr_font_28, fill=WHITE, anchor="lm")
    if not items:
        draw.text((258, top + 36), "暂无", font=sr_font_22, fill=GRAY, anchor="lm")
        return top + 110
    for index, item in enumerate(items[:12]):
        if isinstance(item, dict):
            value = item.get("name") or _value(item, "base_type", "name") or "-"
            if title == "获得祝福" and isinstance(item.get("items"), list):
                value = f"{value} x{len(item['items'])}"
            value = str(value)
        else:
            value = str(item)
        x = 78 + index % 3 * 250
        y = top + 82 + index // 3 * 40
        draw.text((x, y), value[:14], font=sr_font_20, fill=GRAY, anchor="lm")
    return top + 70 + max(1, math.ceil(len(items[:12]) / 3)) * 40 + 20


async def _draw_overview(uid: str, data: dict[str, Any]) -> bytes:
    img = _base_image(1120)
    draw = ImageDraw.Draw(img)
    basic = data.get("basic", {})
    draw.text((58, 65), "差分宇宙 - 乐园漫记", font=sr_font_42, fill=WHITE, anchor="lm")
    draw.text((842, 68), f"UID {uid}", font=sr_font_22, fill=GRAY, anchor="rm")
    _stat(draw, 52, str(basic.get("season_level", "-")), "拟合等级")
    _stat(
        draw,
        325,
        f"{basic.get('weekly_score', '-')}/{basic.get('weekly_score_max', '-')}",
        "本期额外拟合值",
    )
    _stat(
        draw,
        598,
        str(_value(basic, "normal_record_brief", "title")),
        "当前星阶",
    )

    _panel(draw, (52, 262, 848, 382))
    draw.text((78, 303), "奖励领取情况", font=sr_font_30, fill=WHITE, anchor="lm")
    draw.text(
        (78, 348),
        f"可能性画廊  {basic.get('possibility_gallery_finished', '-')}/{basic.get('possibility_gallery_total', '-')}",
        font=sr_font_22,
        fill=GRAY,
        anchor="lm",
    )
    draw.text(
        (455, 348),
        f"稳态数组  {basic.get('season_task_finished', '-')}/{basic.get('season_task_total', '-')}",
        font=sr_font_22,
        fill=GRAY,
        anchor="lm",
    )

    normal_records = _records(data, "normal_detail")
    draw.text((52, 435), "常规演算 - 最新通关队伍", font=sr_font_30, fill=WHITE, anchor="lm")
    if normal_records:
        record = normal_records[0]
        draw.text(
            (848, 435),
            f"{_format_time(record.get('finish_time'))}  X{_value(record, 'common_info_v2', 'level')}",
            font=sr_font_20,
            fill=GRAY,
            anchor="rm",
        )
        await _draw_lineup(img, record.get("final_lineup", []), 468)
    else:
        draw.text((52, 485), "暂无常规演算记录", font=sr_font_22, fill=GRAY, anchor="lm")

    current_week = _value(data, "last_week_detail", default={})
    weekly_records = current_week.get("records", []) if isinstance(current_week, dict) else []
    top = 710
    _panel(draw, (52, top, 848, top + 300))
    draw.text((78, top + 46), "周期演算 - 本期", font=sr_font_30, fill=WHITE, anchor="lm")
    draw.text(
        (78, top + 90),
        str(current_week.get("weekly_name", "暂无周期信息")),
        font=sr_font_22,
        fill=GOLD,
        anchor="lm",
    )
    if weekly_records:
        record = weekly_records[0]
        draw.text(
            (78, top + 137),
            f"最近通关: {_format_time(record.get('finish_time'))}",
            font=sr_font_22,
            fill=GRAY,
            anchor="lm",
        )
        draw.text(
            (78, top + 181),
            f"星阶: X{_value(record, 'common_info_v2', 'level')}   队伍人数: {len(record.get('final_lineup', []))}",
            font=sr_font_22,
            fill=GRAY,
            anchor="lm",
        )
    else:
        draw.text((78, top + 150), "暂无周期演算记录", font=sr_font_22, fill=GRAY, anchor="lm")
    draw.text((450, 1062), "StarRailUID", font=sr_font_20, fill=GRAY, anchor="mm")
    return await convert_img(img)


async def _draw_record(
    uid: str,
    data: dict[str, Any],
    title: str,
    record: dict[str, Any],
    index: int,
    total: int,
) -> bytes:
    formula_list = record.get("formula_list", [])
    miracles = record.get("miracles", [])
    buffs = record.get("buffs", [])
    rooms = record.get("room_card_list", [])
    height = 1020
    for items in (formula_list, miracles, buffs, rooms):
        height += 70 + max(1, math.ceil(len(items[:12]) / 3)) * 40
    img = _base_image(height)
    draw = ImageDraw.Draw(img)
    basic = data.get("basic", {})
    draw.text((52, 62), f"差分宇宙 - {title}", font=sr_font_42, fill=WHITE, anchor="lm")
    draw.text((848, 62), f"UID {uid}", font=sr_font_22, fill=GRAY, anchor="rm")
    _stat(draw, 52, str(basic.get("season_level", "-")), "拟合等级")
    _stat(
        draw,
        325,
        f"{basic.get('weekly_score', '-')}/{basic.get('weekly_score_max', '-')}",
        "本期额外拟合值",
    )
    _stat(draw, 598, f"{index}/{total}", "挑战记录")

    draw.text((52, 286), "探索队伍", font=sr_font_30, fill=WHITE, anchor="lm")
    draw.text(
        (848, 286),
        f"{_format_time(record.get('finish_time'))}  X{_value(record, 'common_info_v2', 'level')}",
        font=sr_font_20,
        fill=GRAY,
        anchor="rm",
    )
    await _draw_lineup(img, record.get("final_lineup", []), 315)

    persona = record.get("persona_style", {})
    _panel(draw, (52, 540, 848, 650))
    draw.text((78, 582), "面具", font=sr_font_28, fill=WHITE, anchor="lm")
    draw.text(
        (200, 582),
        f"{persona.get('title', '暂无')} Lv.{persona.get('style_level', '-')}",
        font=sr_font_22,
        fill=GOLD,
        anchor="lm",
    )
    draw.text(
        (78, 620),
        str(persona.get("desc", ""))[:42],
        font=sr_font_20,
        fill=GRAY,
        anchor="lm",
    )

    top = 690
    top = _draw_item_list(draw, "已展开方程", formula_list, top)
    top = _draw_item_list(draw, "获得奇物", miracles, top)
    top = _draw_item_list(draw, "获得祝福", buffs, top)
    _draw_item_list(draw, "沿途站点", rooms, top)
    return await convert_img(img)


async def draw_rogue_tourn_img(
    uid: str,
    mode: str = "overview",
    index: int = 1,
) -> bytes | str:
    data = await mys_api.get_rogue_tourn_info(uid)
    if isinstance(data, int):
        return get_error(data)
    if not isinstance(data, dict) or not isinstance(data.get("basic"), dict):
        return "未获取到差分宇宙数据"
    if mode == "overview":
        result = await _draw_overview(uid, data)
        logger.info("[查询差分宇宙]绘图已完成,等待发送!")
        return result

    mode_map = {
        "normal": ("normal_detail", "常规演算"),
        # 米游社当前将本期与上期周期记录放在相反字段中。
        "current_week": ("last_week_detail", "周期演算 (本期)"),
        "last_week": ("cur_week_detail", "周期演算 (上期)"),
    }
    detail_key, title = mode_map[mode]
    records = _records(data, detail_key)
    if not records:
        return f"你还没有挑战{title}~"
    if index < 1 or index > len(records):
        return f"{title}仅有{len(records)}条记录"
    result = await _draw_record(uid, data, title, records[index - 1], index, len(records))
    logger.info("[查询差分宇宙]绘图已完成,等待发送!")
    return result
