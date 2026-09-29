import asyncio
from datetime import datetime
import json
from pathlib import Path

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_pic_with_ring, get_color_bg

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

CHANGE_MAP = {
    "始发跃迁": "begin",
    "群星跃迁": "normal",
    "角色跃迁": "char",
    "光锥跃迁": "weapon",
    "角色联动跃迁": "char_collabo",
    "光锥联动跃迁": "weapon_collabo",
}
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
NORMAL_LIST = [
    "彦卿",
    "白露",
    "姬子",
    "瓦尔特",
    "布洛妮娅",
    "克拉拉",
    "杰帕德",
    "银河铁道之夜",
    "以世界之名",
    "但战斗还未结束",
    "制胜的瞬间",
    "无可取代的东西",
    "时节不居",
    "如泥酣眠",
]

UP_LIST = {
    "希儿": [(2021, 2, 17, 18, 0, 0), (2025, 4, 9, 5, 59, 59)],
    "刃": [(2021, 2, 17, 18, 0, 0), (2025, 4, 9, 5, 59, 59)],
    "符玄": [(2021, 2, 17, 18, 0, 0), (2025, 4, 9, 5, 59, 59)],
    "云璃": [(2021, 2, 17, 18, 0, 0), (2026, 4, 22, 5, 59, 59)],
    "银枝": [(2021, 2, 17, 18, 0, 0), (2026, 4, 22, 5, 59, 59)],
    "银狼": [(2021, 2, 17, 18, 0, 0), (2026, 4, 22, 5, 59, 59)],
}


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


def check_up(name: str, _time: str) -> bool:
    for char in UP_LIST:
        if char == name:
            time = UP_LIST[char]
            e_time = datetime(*time[1])
            gacha_time = datetime.strptime(_time, "%Y-%m-%d %H:%M:%S")
            if gacha_time > e_time:
                return False
            return True
    return True


def _is_same_five_star_record(
    o: dict[str, str | int | bool],
    n: dict[str, str | int | bool],
) -> bool:
    o_id = str(o["id"]) if "id" in o else ""
    n_id = str(n["id"]) if "id" in n else ""
    if o_id and n_id and o_id == n_id:
        return True
    o_name = str(o["name"]) if "name" in o else ""
    n_name = str(n["name"]) if "name" in n else ""
    if o_name and n_name and o_name == n_name and len(o_id) >= 10 and len(n_id) >= 10:
        return o_id[:10] == n_id[:10]
    return False


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

    if not gacha_data:
        data_time_val = str(wx_data["data_time"]) if "data_time" in wx_data else ""
        gacha_data = {
            "uid": str(uid),
            "data_time": data_time_val,
            "normal_gacha_num": 0,
            "begin_gacha_num": 0,
            "char_gacha_num": 0,
            "weapon_gacha_num": 0,
            "char_collabo_gacha_num": 0,
            "weapon_collabo_gacha_num": 0,
            "data": {},
        }

    # 数据初始化
    total_data = {}
    for i in [
        "群星跃迁",
        "始发跃迁",
        "角色跃迁",
        "光锥跃迁",
        "角色联动跃迁",
        "光锥联动跃迁",
    ]:
        total_data[i] = {
            "total": 0,  # 五星总数
            "avg": 0,  # 抽卡平均数
            "avg_up": 0,  # up平均数
            "remain": 0,  # 已xx抽未出金
            "r_num": [],  # 不包含首位的抽卡数量
            "e_num": [],  # 包含首位的up抽卡数量
            "up_list": [],  # 抽到的UP列表(不包含首位)
            "normal_list": [],  # 抽到的五星列表(不包含首位)
            "list": [],  # 抽到的五星列表
            "time_range": "",  # 抽卡时间
            "all_time": 0,  # 抽卡总计秒数
            "type": "一般型",  # 抽卡类型: 随缘型, 氪金型, 规划型, 仓鼠型, 佛系型
            "short_gacha_data": {"time": 0, "num": 0},
            "long_gacha_data": {"time": 0, "num": 0},
        }
        # 拿到数据列表
        raw_pool_data = (
            gacha_data["data"] if "data" in gacha_data and isinstance(gacha_data["data"], dict) else {}
        )
        data_list = raw_pool_data[i] if i in raw_pool_data and isinstance(raw_pool_data[i], list) else []
        # 初始化开关
        is_not_first = True
        # 开始初始化抽卡数
        num = 1
        # 从后面开始循环
        temp_time = datetime(2023, 4, 26, 8, 0, 0)
        for index, data in enumerate(data_list[::-1]):
            # 计算抽卡时间跨度
            if index == 0:
                total_data[i]["time_range"] = data["time"]
            if index == len(data_list) - 1:
                _fm = "%Y-%m-%d %H:%M:%S"
                t1 = datetime.strptime(data["time"], _fm)
                t2 = datetime.strptime(total_data[i]["time_range"], _fm)
                total_data[i]["all_time"] = (t1 - t2).total_seconds()
                total_data[i]["time_range"] += "~" + data["time"]

            # 计算时间间隔
            if index != 0:
                now_time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
                dis = (now_time - temp_time).total_seconds()
                temp_time = now_time
                if dis <= 5000:
                    total_data[i]["short_gacha_data"]["num"] += 1
                    total_data[i]["short_gacha_data"]["time"] += dis
                elif dis >= 86400:
                    total_data[i]["long_gacha_data"]["num"] += 1
                    total_data[i]["long_gacha_data"]["time"] += dis
            else:
                temp_time = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")

            # 如果这是个五星
            if data["rank_type"] == "5":
                # 抽到这个五星花了多少抽
                data["gacha_num"] = num

                # 判断是否是UP
                if data["name"] in NORMAL_LIST:
                    data["is_up"] = False
                elif data["name"] in UP_LIST:
                    data["is_up"] = check_up(data["name"], data["time"])
                else:
                    data["is_up"] = True

                # 往里加东西
                if is_not_first:
                    total_data[i]["r_num"].append(num)
                    total_data[i]["normal_list"].append(data)
                    if data["is_up"]:
                        total_data[i]["up_list"].append(data)

                # 把这个数据扔到抽到的五星列表内
                total_data[i]["list"].append(data)

                # 判断经过了第一个
                if total_data[i]["list"]:
                    is_not_first = True

                num = 1
                # 五星总数增加1
                total_data[i]["total"] += 1
            else:
                num += 1

        # 计算已多少抽
        total_data[i]["remain"] = num - 1
        old_remain = total_data[i]["remain"]

        # 合并新抽卡记录五星列表
        raw_wx_pool_data = (
            wx_data["data"] if wx_data and "data" in wx_data and isinstance(wx_data["data"], dict) else {}
        )
        wx_pool_list = (
            raw_wx_pool_data[i] if i in raw_wx_pool_data and isinstance(raw_wx_pool_data[i], list) else []
        )
        # wx_pool_list 按最新在最前, 倒序即为时间升序
        wx_chronological = list(reversed(wx_pool_list))

        new_fives: list[dict[str, str | int | bool]] = []
        if wx_chronological:
            if not total_data[i]["list"]:
                new_fives = wx_chronological
            else:
                matched_wx = set()
                old_idx = 0
                for wx_idx, n in enumerate(wx_chronological):
                    for oi in range(old_idx, len(total_data[i]["list"])):
                        if _is_same_five_star_record(total_data[i]["list"][oi], n):
                            matched_wx.add(wx_idx)
                            old_idx = oi + 1
                            break
                new_fives = [
                    wx_chronological[idx] for idx in range(len(wx_chronological)) if idx not in matched_wx
                ]

        for item in new_fives:
            data_item = dict(item)
            data_item["rank_type"] = "5"
            gacha_cnt = (
                data_item["gacha_count"]
                if "gacha_count" in data_item and isinstance(data_item["gacha_count"], int)
                else 0
            )
            data_item["gacha_num"] = gacha_cnt
            if "is_up" not in data_item or data_item["is_up"] is None:
                if data_item["name"] in NORMAL_LIST:
                    data_item["is_up"] = False
                elif data_item["name"] in UP_LIST:
                    t_str = str(data_item["time"]) if "time" in data_item else ""
                    data_item["is_up"] = check_up(str(data_item["name"]), t_str)
                else:
                    data_item["is_up"] = True
            else:
                data_item["is_up"] = bool(data_item["is_up"])

            total_data[i]["list"].append(data_item)
            total_data[i]["r_num"].append(data_item["gacha_num"])
            total_data[i]["normal_list"].append(data_item)
            if data_item["is_up"]:
                total_data[i]["up_list"].append(data_item)
            total_data[i]["total"] += 1

            # 扩展抽卡时间跨度
            if "time" in data_item and isinstance(data_item["time"], str) and data_item["time"]:
                if not total_data[i]["time_range"]:
                    total_data[i]["time_range"] = data_item["time"]
                elif "~" in total_data[i]["time_range"]:
                    start_t = total_data[i]["time_range"].split("~")[0]
                    total_data[i]["time_range"] = f"{start_t}~{data_item['time']}"
                else:
                    total_data[i]["time_range"] += f"~{data_item['time']}"

        # 无旧数据时补齐 time_range 区间
        if not data_list and total_data[i]["list"]:
            first_item = total_data[i]["list"][0]
            last_item = total_data[i]["list"][-1]
            first_t = str(first_item["time"]) if "time" in first_item else ""
            last_t = str(last_item["time"]) if "time" in last_item else ""
            if first_t and last_t and first_t != last_t:
                total_data[i]["time_range"] = f"{first_t}~{last_t}"
            elif first_t:
                total_data[i]["time_range"] = first_t

        # 已xx抽未出金取新的抽卡记录
        if wx_data and "pity_counts" in wx_data and isinstance(wx_data["pity_counts"], dict):
            if i in wx_data["pity_counts"]:
                total_data[i]["remain"] = int(wx_data["pity_counts"][i])

        # 抽卡总数补偿计算
        pool_num_key = f"{CHANGE_MAP[i]}_gacha_num"
        current_gacha_num = int(gacha_data[pool_num_key]) if pool_num_key in gacha_data else 0
        if current_gacha_num == 0 and total_data[i]["r_num"]:
            gacha_data[pool_num_key] = sum(total_data[i]["r_num"]) + total_data[i]["remain"]
        else:
            fresh_pulls = sum(int(item["gacha_num"]) for item in new_fives if "gacha_num" in item)
            if total_data[i]["remain"] > old_remain:
                fresh_pulls += total_data[i]["remain"] - old_remain
            gacha_data[pool_num_key] = current_gacha_num + fresh_pulls

        # 计算平均抽卡数
        if len(total_data[i]["normal_list"]) == 0:
            total_data[i]["avg"] = 0
        else:
            total_data[i]["avg"] = float(
                "{:.2f}".format(sum(total_data[i]["r_num"]) / len(total_data[i]["r_num"]))
            )
        # 计算平均up数量
        if len(total_data[i]["up_list"]) == 0:
            total_data[i]["avg_up"] = 0
        else:
            total_data[i]["avg_up"] = float(
                "{:.2f}".format(sum(total_data[i]["r_num"]) / len(total_data[i]["up_list"]))
            )

        # 计算抽卡类型
        # 如果抽卡总数小于40
        if gacha_data[f"{CHANGE_MAP[i]}_gacha_num"] <= 40:
            total_data[i]["type"] = "佛系型"
        # 如果长时抽卡总数占据了总抽卡数的70%
        elif total_data[i]["long_gacha_data"]["num"] / gacha_data[f"{CHANGE_MAP[i]}_gacha_num"] >= 0.7:
            total_data[i]["type"] = "随缘型"
        # 如果短时抽卡总数占据了总抽卡数的70%
        elif total_data[i]["short_gacha_data"]["num"] / gacha_data[f"{CHANGE_MAP[i]}_gacha_num"] >= 0.7:
            total_data[i]["type"] = "规划型"
        # 如果抽卡数量远远大于标称抽卡数量
        elif total_data[i]["all_time"] / 30000 <= gacha_data[f"{CHANGE_MAP[i]}_gacha_num"]:
            # 如果长时抽卡数量大于短时抽卡数量
            if total_data[i]["long_gacha_data"]["num"] >= total_data[i]["short_gacha_data"]["num"]:
                total_data[i]["type"] = "规划型"
            else:
                total_data[i]["type"] = "氪金型"
        # 如果抽卡数量远远小于标称抽卡数量
        elif total_data[i]["all_time"] / 32000 >= gacha_data[f"{CHANGE_MAP[i]}_gacha_num"] * 2:
            total_data[i]["type"] = "仓鼠型"

    # 有垫抽但尚未出金的卡池也需要展示。
    pools = [
        name
        for name in POOL_ORDER
        if total_data[name]["total"]
        or total_data[name]["remain"]
        or total_data[name]["time_range"]
        or gacha_data[f"{CHANGE_MAP[name]}_gacha_num"]
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
            title = await _compose_pool_title(
                pool_name, pool_data, int(gacha_data[f"{CHANGE_MAP[pool_name]}_gacha_num"])
            )
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
