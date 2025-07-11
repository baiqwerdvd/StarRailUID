import asyncio
from datetime import datetime
import json
from pathlib import Path
from typing import List, Tuple, Union

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_pic_with_ring, get_color_bg

from ..utils.error_reply import prefix
from ..utils.fonts.starrail_fonts import (
    sr_font_20,
    sr_font_24,
    sr_font_28,
    sr_font_38,
    sr_font_40,
)
from ..utils.image.image_tools import _get_event_avatar
from ..utils.name_covert import name_to_avatar_id, name_to_weapon_id
from ..utils.resource.RESOURCE_PATH import (
    CHAR_ICON_PATH,
    PLAYER_PATH,
    WEAPON_PATH,
)

TEXT_PATH = Path(__file__).parent / "texture2d"
EMO_PATH = Path(__file__).parent / "texture2d" / "emo"

# up_tag = Image.open(TEXT_PATH / 'up.png')
Abg3_img = Image.open(TEXT_PATH / "Abg3.png")
bg1_img = Image.open(TEXT_PATH / "bg1.png")

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
HOMO_TAG = ["非到极致", "运气不好", "平稳保底", "小欧一把", "欧狗在此"]
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
}


async def _draw_card(
    img: Image.Image,
    xy_point: Tuple[int, int],
    card_type: str,
    name: str,
    gacha_num: int,
    is_up: bool,
):
    card_img = Image.open(TEXT_PATH / "char_bg.png")
    card_img_draw = ImageDraw.Draw(card_img)
    point = (47, 31)
    text_point = (100, 165)
    if card_type == "角色":
        _id = await name_to_avatar_id(name)
        item_pic = Image.open(CHAR_ICON_PATH / f"{_id}.png")
        item_pic = item_pic.convert("RGBA").resize((105, 105))
    else:
        name = await name_to_weapon_id(name)
        # _id = await weapon_id_to_en_name(name)
        item_pic = Image.open(WEAPON_PATH / f"{name}.png")
        item_pic = item_pic.convert("RGBA").resize((124, 124))
        point = (37, 24)
    card_img.paste(item_pic, point, item_pic)
    if gacha_num >= 81:
        text_color = red_color
    elif gacha_num <= 55:
        text_color = green_color
    else:
        text_color = brown_color
    card_img_draw.text(text_point, f"{gacha_num}抽", text_color, sr_font_24, "mm")
    if is_up:
        logger.info(f"up: {name}")
        # card_img.paste(up_tag, (47, -2), up_tag)
    img.paste(card_img, xy_point, card_img)


async def random_emo_pic(level: int) -> Image.Image:
    emo_fold = EMO_PATH / f"3000{level}.png"
    return Image.open(emo_fold)


async def get_level_from_list(ast: int, lst: List) -> int:
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
            s_time = datetime(*time[0])
            e_time = datetime(*time[1])
            gacha_time = datetime.strptime(_time, "%Y-%m-%d %H:%M:%S")
            if gacha_time > e_time:
                return False
            return True
    return True


async def draw_gachalogs_img(uid: str, ev: Event) -> Union[bytes, str]:
    path = PLAYER_PATH / str(uid) / "gacha_logs.json"
    if not path.exists():
        return f"你还没有跃迁数据噢~\n请使用命令`{prefix}导入抽卡链接`更新跃迁数据~"
    with Path.open(path, encoding="UTF-8") as f:
        gacha_data = json.load(f)

    # 数据初始化
    total_data = {}
    for i in ["群星跃迁", "始发跃迁", "角色跃迁", "光锥跃迁", "角色联动跃迁", "光锥联动跃迁"]:
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
        data_list = gacha_data["data"][i]
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

    # 常量偏移数据
    single_y = 170

    # 计算图片尺寸
    normal_y = (1 + ((total_data["群星跃迁"]["total"] - 1) // 5)) * single_y
    begin_y = (1 + ((total_data["始发跃迁"]["total"] - 1) // 5)) * single_y
    char_y = (1 + ((total_data["角色跃迁"]["total"] - 1) // 5)) * single_y
    weapon_y = (1 + ((total_data["光锥跃迁"]["total"] - 1) // 5)) * single_y
    char_collab_y = (1 + ((total_data["角色联动跃迁"]["total"] - 1) // 5)) * single_y
    weapon_collab_y = (1 + ((total_data["光锥联动跃迁"]["total"] - 1) // 5)) * single_y

    # 获取背景图片各项参数
    char_pic = await _get_event_avatar(ev)
    char_pic = await draw_pic_with_ring(char_pic, 206, None, False)

    # 获取背景图片各项参数
    img = Abg3_img.copy()
    img = await get_color_bg(
        800,
        1600 + 400 + normal_y + char_y + weapon_y + char_collab_y + weapon_collab_y + begin_y,
    )
    gacha_title = bg1_img.copy()
    gacha_title.paste(char_pic, (297, 81), char_pic)
    img.paste(gacha_title, (0, 0), gacha_title)
    img_draw = ImageDraw.Draw(img)
    img_draw.text((400, 345), f"UID {uid}", white_color, sr_font_28, "mm")

    # 处理title
    # {'total': 0, 'avg': 0, 'remain': 0, 'list': []}
    type_list = ["角色跃迁", "光锥跃迁", "角色联动跃迁", "光锥联动跃迁", "群星跃迁", "始发跃迁"]
    y_extend = 0
    level = 3
    for index, i in enumerate(type_list):
        title = Image.open(TEXT_PATH / "bg2.png")
        if i == "群星跃迁":
            level = await get_level_from_list(total_data[i]["avg"], [54, 61, 67, 73, 80])
        elif i == "始发跃迁":
            level = await get_level_from_list(total_data[i]["avg"], [10, 20, 30, 40, 50])
        elif i == "光锥跃迁":
            level = await get_level_from_list(total_data[i]["avg_up"], [62, 75, 88, 99, 111])
        elif i == "角色跃迁":
            level = await get_level_from_list(total_data[i]["avg_up"], [74, 87, 99, 105, 120])
        elif i == "光锥联动跃迁":
            level = await get_level_from_list(total_data[i]["avg_up"], [62, 75, 88, 99, 111])
        elif i == "角色联动跃迁":
            level = await get_level_from_list(total_data[i]["avg_up"], [74, 87, 99, 105, 120])
        else:
            continue

        emo_pic = await random_emo_pic(level)
        emo_pic = emo_pic.resize((195, 195))
        title.paste(emo_pic, (500, 123), emo_pic)
        title_draw = ImageDraw.Draw(title)
        # 卡池
        title_draw.text((110, 73), i, whole_white_color, sr_font_38, "lm")
        # 抽卡时间
        if total_data[i]["time_range"]:
            time_range = total_data[i]["time_range"]
        else:
            time_range = "暂未抽过卡!"
        title_draw.text((78, 340), time_range, brown_color, sr_font_20, "lm")
        # 平均抽卡数量
        title_draw.text(
            (143, 215),
            str(total_data[i]["avg"]),
            first_color,
            sr_font_40,
            "mm",
        )
        # 平均up
        title_draw.text(
            (280, 215),
            str(total_data[i]["avg_up"]),
            first_color,
            sr_font_40,
            "mm",
        )
        # 抽卡总数
        title_draw.text(
            (413, 215),
            str(gacha_data[f"{CHANGE_MAP[i]}_gacha_num"]),
            first_color,
            sr_font_40,
            "mm",
        )
        # 已抽数
        title_draw.text(
            (333, 75),
            str(total_data[i]["remain"]),
            red_color,
            sr_font_28,
            "mm",
        )
        y_extend += (
            (1 + ((total_data[type_list[index - 1]]["total"] - 1) // 5)) * single_y if index != 0 else 0
        )
        y = 350 + index * 400 + y_extend
        img.paste(title, (0, y), title)
        tasks = []
        for item_index, item in enumerate(reversed(total_data[i]["list"])):
            item_x = (item_index % 5) * 138 + 25
            item_y = (item_index // 5) * single_y + y + 355
            xy_point = (item_x, item_y)
            tasks.append(
                _draw_card(
                    img,
                    xy_point,
                    item["item_type"],
                    item["name"],
                    item["gacha_num"],
                    item["is_up"],
                )
            )
        await asyncio.gather(*tasks)
        tasks.clear()

    # 发送图片
    res = await convert_img(img)
    logger.info("[查询抽卡]绘图已完成,等待发送!")
    # res = 123
    return res
