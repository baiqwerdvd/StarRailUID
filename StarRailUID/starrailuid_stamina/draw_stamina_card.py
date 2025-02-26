import asyncio
from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.utils.database.models import GsBind, GsUser
from gsuid_core.utils.image.convert import convert_img
from httpx import AsyncClient

from ..sruid_utils.api.mys.models import Expedition
from ..starrailuid_config.sr_config import srconfig
from ..utils.error_reply import get_error as get_error_msg
from ..utils.fonts.starrail_fonts import (
    sr_font_22,
    sr_font_24,
    sr_font_26,
    sr_font_36,
    sr_font_50,
)
from ..utils.image.image_tools import get_simple_bg
from ..utils.mys_api import mys_api

use_widget = srconfig.get_config("WidgetResin").data

TEXT_PATH = Path(__file__).parent / "texture2D"

note_bg = Image.open(TEXT_PATH / "note_bg.png")
note_travel_bg = Image.open(TEXT_PATH / "note_travel_bg.png")
warn_pic = Image.open(TEXT_PATH / "warn.png")

based_w = 700
based_h = 1200
white_overlay = Image.new("RGBA", (based_w, based_h), (255, 251, 242, 225))

first_color = (29, 29, 29)
second_color = (98, 98, 98)
white_color = (255, 255, 255)
green_color = (15, 196, 35)
orange_color = (237, 115, 61)
red_color = (235, 61, 75)


def seconds2hours(seconds: int) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


async def download_image(url: str) -> Image.Image:
    async with AsyncClient() as session:
        response = await session.get(url)
        img_data = response.read()
        return Image.open(BytesIO(img_data))


async def _draw_task_img(
    img: Image.Image,
    img_draw: ImageDraw.ImageDraw,
    index: int,
    char: Optional[Expedition],
):
    if char is not None:
        expedition_name = char.name
        remaining_time: str = seconds2hours(char.remaining_time)
        note_travel_img = note_travel_bg.copy()
        for i in range(2):
            avatar_url = char.avatars[i]
            image = await download_image(avatar_url)
            char_pic = image.convert("RGBA").resize(
                (40, 40),
                Image.Resampling.LANCZOS,  # type: ignore
            )
            note_travel_img.paste(char_pic, (495 + 68 * i, 20), char_pic)
        img.paste(note_travel_img, (0, 790 + index * 80), note_travel_img)
        if char.status == "Finished":
            status_mark = "待收取"
        else:
            status_mark = str(remaining_time)
        img_draw.text(
            (120, 830 + index * 80),
            expedition_name,
            font=sr_font_22,
            fill=white_color,
            anchor="lm",
        )
        img_draw.text(
            (380, 830 + index * 80),
            status_mark,
            font=sr_font_22,
            fill=white_color,
            anchor="mm",
        )
    else:
        note_travel_img = note_travel_bg.copy()
        img.paste(note_travel_img, (0, 790 + index * 80), note_travel_img)
        img_draw.text(
            (120, 830 + index * 80),
            "等待加入探索队列...",
            font=sr_font_22,
            fill=white_color,
            anchor="lm",
        )


async def get_stamina_img(bot_id: str, user_id: str):
    try:
        uid_list = await GsBind.get_uid_list_by_game(user_id, bot_id, "sr")
        logger.info(f"[每日信息]UID: {uid_list}")
        if uid_list is None:
            return "请先绑定一个UID再来查询哦~"
        # 进行校验UID是否绑定CK
        useable_uid_list = []
        for uid in uid_list:
            status = await GsUser.get_user_cookie_by_uid(uid, "sr")
            if status is not None:
                useable_uid_list.append(uid)
        logger.info(f"[每日信息]可用UID: {useable_uid_list}")
        if len(useable_uid_list) == 0:
            return "请先绑定一个可用CK & UID再来查询哦~"
        # 开始绘图任务
        task = []
        img = Image.new("RGBA", (based_w * len(useable_uid_list), based_h), (0, 0, 0, 0))
        for uid_index, uid in enumerate(useable_uid_list):
            task.append(_draw_all_stamina_img(img, uid, uid_index))
        await asyncio.gather(*task)
        res = await convert_img(img)
        logger.info("[查询每日信息]绘图已完成,等待发送!")
    except TypeError:
        logger.exception("[查询每日信息]绘图失败!")
        res = "你绑定过的UID中可能存在过期CK~请重新绑定一下噢~"

    return res


async def _draw_all_stamina_img(img: Image.Image, uid: str, index: int):
    stamina_img = await draw_stamina_img(uid)
    img.paste(stamina_img, (700 * index, 0), stamina_img)


def get_error(img: Image.Image, uid: str, daily_data: int):
    img_draw = ImageDraw.Draw(img)
    img.paste(warn_pic, (0, 0), warn_pic)
    # 写UID
    img_draw.text(
        (350, 680),
        f"UID{uid}",
        font=sr_font_26,
        fill=first_color,
        anchor="mm",
    )
    error_text = get_error_msg(daily_data)
    img_draw.text(
        (350, 650),
        f"{error_text}, 错误码{daily_data}",
        font=sr_font_26,
        fill=red_color,
        anchor="mm",
    )
    return img


async def seconds2hours_zhcn(seconds: int) -> str:
    m, _ = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}小时{m:02d}分"


async def draw_stamina_img(sr_uid: str) -> Image.Image:
    img = await get_simple_bg(based_w, based_h)
    img.paste(white_overlay, (0, 0), white_overlay)

    # 获取数据
    if use_widget and int(str(sr_uid)[0]) <= 5:
        _daily_data = await mys_api.get_widget_stamina_data(sr_uid)
        if isinstance(_daily_data, int):
            return get_error(img, sr_uid, _daily_data)
        # daily_data = transform_fake_resin(_daily_data)
        daily_data = _daily_data
    else:
        daily_data = await mys_api.get_sr_daily_data(sr_uid)
        if isinstance(daily_data, int):
            return get_error(img, sr_uid, daily_data)

    # nickname and level
    # deal with hoyolab with no nickname and level api
    if int(str(sr_uid)[0]) < 6:
        role_basic_info = await mys_api.get_role_basic_info(sr_uid)
        if isinstance(role_basic_info, int):
            return get_error(img, sr_uid, role_basic_info)
        nickname = role_basic_info.nickname
        level = role_basic_info.level
    else:
        nickname = "开拓者"
        level = "0"

    # 开拓力
    stamina = daily_data.current_stamina
    max_stamina = daily_data.max_stamina
    stamina_str = f"{stamina}/{max_stamina}"
    stamina_percent = stamina / max_stamina
    if stamina_percent > 0.8:
        stamina_color = red_color
    else:
        stamina_color = second_color
    stamina_recovery_time = await seconds2hours_zhcn(
        daily_data.stamina_recover_time,
    )

    img.paste(note_bg, (0, 0), note_bg)
    img_draw = ImageDraw.Draw(img)

    # 派遣
    task_task = []
    for i in range(4):
        char = daily_data.expeditions[i] if i < len(daily_data.expeditions) else None
        task_task.append(_draw_task_img(img, img_draw, i, char))
    await asyncio.gather(*task_task)

    # 绘制树脂圆环
    ring_pic = Image.open(TEXT_PATH / "ring.apng")
    percent = round(stamina_percent * 89) if round(stamina_percent * 89) <= 89 else 89
    ring_pic.seek(percent)
    img.paste(ring_pic, (0, 5), ring_pic)

    # 写树脂剩余时间
    img_draw.text(
        (350, 490),
        f"还剩{stamina_recovery_time}",
        font=sr_font_24,
        fill=stamina_color,
        anchor="mm",
    )
    # 写Nickname
    img_draw.text(
        (350, 139),
        nickname,
        font=sr_font_36,
        fill=white_color,
        anchor="mm",
    )
    # 写开拓等级
    img_draw.text(
        (350, 190),
        f"开拓等级{level}",
        font=sr_font_24,
        fill=white_color,
        anchor="mm",
    )
    # 写UID
    img_draw.text(
        (350, 663),
        f"UID{sr_uid}",
        font=sr_font_26,
        fill=first_color,
        anchor="mm",
    )
    # 写树脂
    img_draw.text(
        (350, 450),
        stamina_str,
        font=sr_font_50,
        fill=first_color,
        anchor="mm",
    )

    return img
