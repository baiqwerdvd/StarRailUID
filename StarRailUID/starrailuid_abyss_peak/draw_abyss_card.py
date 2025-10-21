from pathlib import Path
from typing import Union

import msgspec
from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.utils.error_reply import get_error
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_pic_with_ring

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
from ..utils.resource.get_pic_from import get_roleinfo_icon, get_abyss_peak_img

TEXT_PATH = Path(__file__).parent / "texture2D"
white_color = (255, 255, 255)
gray_color = (175, 175, 175)
gold_color = (243, 214, 148)
img_bg = Image.open(TEXT_PATH / "bg.jpg")
title_bg = Image.open(TEXT_PATH / "title_bg.png").convert("RGBA")
title_fg = Image.open(TEXT_PATH / "title_fg.png").convert("RGBA")
star1 = Image.open(TEXT_PATH / "star1.png").convert("RGBA")
star1e = Image.open(TEXT_PATH / "star1_empty.png").convert("RGBA")
star2 = Image.open(TEXT_PATH / "star2.png").convert("RGBA")
star2e = Image.open(TEXT_PATH / "star2_empty.png").convert("RGBA")
bar = Image.open(TEXT_PATH / "bar.png").convert("RGBA")
king_card = Image.open(TEXT_PATH / "king_card.png").convert("RGBA")
knight_card = Image.open(TEXT_PATH / "knight_card.png").convert("RGBA")
knight_card_fg = Image.open(TEXT_PATH / "knight_card_fg2.png").convert("RGBA")
monster_card = Image.open(TEXT_PATH / "monster_card.png").convert("RGBA")
banner = Image.open(TEXT_PATH / "banner.png").convert("RGBA")
char_bg_4 = Image.open(TEXT_PATH / "char4_bg.png").convert("RGBA")
char_bg_5 = Image.open(TEXT_PATH / "char5_bg.png").convert("RGBA")
level_cover = Image.open(TEXT_PATH / "level_cover.png").convert("RGBA")
rank_bg = Image.open(TEXT_PATH / "rank_bg.png").convert("RGBA")
boss_img_info = {104: {"scale": 0.6, "pos": (682, 29)}}


async def _draw_char(char: AbyssAvatar) -> Image.Image:
    char_bg = (char_bg_4 if char.rarity == 4 else char_bg_5).copy()
    char_draw = ImageDraw.Draw(char_bg)
    char_icon = (await get_roleinfo_icon(char.icon)).resize((150, 170))
    element_icon = elements[char.element]
    char_bg.paste(char_icon, (24, 16), mask=char_icon)
    char_bg.paste(level_cover, (0, 0), mask=level_cover)
    char_bg.paste(element_icon, (35, 25), mask=element_icon)
    if char.rank > 0:
        char_bg.paste(rank_bg, (150, 16), mask=rank_bg)
        char_draw.text(
            (162, 31),
            f"{char.rank}",
            font=sr_font_22,
            fill=white_color,
            anchor="mm",
        )
    char_draw.text((100, 165), f"等级 {char.level}", white_color, sr_font_22, "mm")
    return char_bg


async def _draw_chars(chars: list[AbyssAvatar]) -> Image.Image:
    chars_bg = Image.new("RGBA", (650, 180), (255, 255, 255, int(255 * 0.3)))
    posx = -15
    for i, char in enumerate(chars):
        char_img = await _draw_char(char)
        chars_bg.paste(char_img, (posx + i * 160, -10), char_img)
    return chars_bg


async def _draw_king_record_card(boss_info, boss_record) -> Image.Image:
    king = king_card.copy()
    king_draw = ImageDraw.Draw(king)
    boss = await get_abyss_peak_img(f"{boss_info.maze_id}.png", boss_info.icon)
    boss = boss.resize((int(boss.width * boss_img_info[104]["scale"]), int(boss.height * boss_img_info[104]["scale"])))
    king.paste(boss, boss_img_info[104]["pos"], mask=boss)
    king_draw.text((140, 67), boss_info.name_mi18n, white_color, sr_font_34, "lm")
    king_draw.text((270, 137), str(boss_record.round_num), gold_color, sr_font_28, "rm")
    for i in range(3):
        if i < boss_record.star_num:
            king.paste(star1, (295 + i * 40, 120), star1)
        else:
            king.paste(star1e, (295 + i * 40, 120), star1e)
    chars_bg = await _draw_chars(boss_record.avatars)
    king.paste(chars_bg, (105, 170), chars_bg)
    king_draw.text((180, 408), f"裁决现象: {boss_record.buff.name_mi18n}", white_color, sr_font_28, "lm")
    buff_img = (await get_abyss_peak_img(f"{boss_record.buff.id}.png", boss_record.buff.icon)).resize((50, 50))
    king.paste(buff_img, (120, 380), mask=buff_img)
    return king


async def _draw_knight_record_card(mob_info, mob_record) -> Image.Image:
    bg = knight_card_fg.copy()
    bg_draw = ImageDraw.Draw(bg)
    bg_draw.text((60, 30), mob_info.name, white_color, sr_font_30, "lm")
    bg_draw.text((460, 30), "已通关", gold_color, sr_font_22, "lm")
    for i in range(3):
        if i < mob_record.star_num:
            bg.paste(star2, (560 + i * 40, 16), star2)
        else:
            bg.paste(star2e, (560 + i * 40, 16), star2e)
    bg_draw.text((790, 33), str(mob_record.round_num), gold_color, sr_font_22, "lm")
    mons_bg = Image.new("RGBA", (140, 180), (255, 255, 255, int(255 * 0.3)))
    bg.paste(mons_bg, (680, 70), mons_bg)
    bg.paste(monster_card, (680, 70), monster_card)
    bg_draw.text((757, 215), mob_info.name, white_color, sr_font_22, "mm")
    chars_bg = await _draw_chars(mob_record.avatars)
    bg.paste(chars_bg, (24, 60), chars_bg)
    bg_draw.text((625, 260), f"{mob_record.challenge_time.year}.{mob_record.challenge_time.month:02d}.{mob_record.challenge_time.day:02d} {mob_record.challenge_time.hour:02d}:{mob_record.challenge_time.minute:02d}", white_color, sr_font_22, "lm")
    mob_img = (await get_abyss_peak_img(f"{mob_info.maze_id}.png", mob_info.monster_icon)).resize((100, 100))
    bg.paste(mob_img, (700, 93), mask=mob_img)
    return bg


async def _draw_knight_records_card(mob_infos, mob_records) -> Image.Image:
    knight = knight_card.copy()
    for i in range(3):
        img = await _draw_knight_record_card(mob_infos[i], mob_records[i])
        knight.paste(img, (90, 25 + 275 * i), img)
    return knight


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
    if not len(raw_abyss_data.challenge_peak_records):
        return f"你还没有挑战本期异相仲裁!\n可以使用[{prefix}上期异相仲裁]命令查询上期~"
    
    challenge_records = raw_abyss_data.challenge_peak_records[0]
    challenge_breif = raw_abyss_data.challenge_peak_best_record_brief
        
    img = img_bg.copy()
    
    # 获取头像
    char_pic = await _get_event_avatar(ev)
    char_pic = await draw_pic_with_ring(char_pic, 100, None, False)
    
    img.paste(char_pic, (80, 220), char_pic)
    img.paste(title_bg, (0, 0), title_bg)
    img.paste(title_fg, (0, 0), title_fg)
    
    img_draw = ImageDraw.Draw(img)
    img_draw.text((237, 250), "开拓者", white_color, sr_font_40, "lm")
    img_draw.text((237, 300), f"UID{uid}", white_color, sr_font_28, "lm")
    img_draw.text((745, 307), f"v{challenge_records.group.game_version}", white_color, sr_font_32, "lm")
    
    # 统计信息
    img.paste(bar, (0, 390), bar)
    img_draw.text((220, 450), f"x {challenge_breif.boss_stars}", white_color, sr_font_28, "lm")
    img_draw.text((220, 500), f"x {challenge_breif.mob_stars}", white_color, sr_font_28, "lm")
    img_draw.text((328, 453), challenge_records.group.name_mi18n, white_color, sr_font_34, "lm")
    img_draw.text((470, 503), str(challenge_breif.total_battle_num), white_color, sr_font_30, "lm")
    rank_icon = (await get_abyss_peak_img(f"{challenge_breif.challenge_peak_rank_icon_type}.png", challenge_breif.challenge_peak_rank_icon)).resize((80, 80))
    img.paste(rank_icon, (68, 438), rank_icon)
    
    img.paste(banner, (-50, 580), banner)
    img_draw.text((450, 615), "王棋战绩", white_color, sr_font_34, "mm")
    king_record = await _draw_king_record_card(challenge_records.boss_info, challenge_records.boss_record)
    img.paste(king_record, (-45, 650), king_record)

    img.paste(banner, (-50, 1135), banner)
    img_draw.text((450, 1170), "骑士战绩", white_color, sr_font_34, "mm")
    knight_record = await _draw_knight_records_card(challenge_records.mob_infos, challenge_records.mob_records)
    img.paste(knight_record, (-45, 1190), knight_record)
    
    res = await convert_img(img)
    logger.info("[查询异相仲裁信息]绘图已完成,等待发送!")
    return res
