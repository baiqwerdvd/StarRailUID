import asyncio
from pathlib import Path
from typing import Dict, List, Tuple, Union

from PIL import Image, ImageDraw
from starrail_damage_cal.to_data import api_to_dict
from gsuid_core.utils.image.convert import convert_img
from starrail_damage_cal.map.SR_MAP_PATH import avatarId2Name
from gsuid_core.utils.image.image_tools import crop_center_img

from ..utils.fonts.first_world import fw_font_28
from ..utils.map.name_covert import avatar_id_to_char_star
from ..utils.resource.RESOURCE_PATH import PLAYER_PATH, CHAR_PREVIEW_PATH
from ..utils.fonts.starrail_fonts import sr_font_24, sr_font_30, sr_font_58

half_color = (255, 255, 255, 120)
first_color = (29, 29, 29)
second_color = (67, 61, 56)
white_color = (247, 247, 247)
gray_color = (175, 175, 175)

TEXT_PATH = Path(__file__).parent / 'texture2D'
char_mask = Image.open(TEXT_PATH / 'ring_mask.png')
char_bg_mask = Image.open(TEXT_PATH / 'char_bg_mask.png')
tag = Image.open(TEXT_PATH / 'tag.png')
footbar = Image.open(TEXT_PATH / 'footbar.png')
pic_500 = Image.open(TEXT_PATH / '500.png')


async def api_to_card(uid: str) -> Union[Tuple[bytes, List[str]], bytes]:
    char_id_list, _ = await api_to_dict(
        uid,
        save_path=PLAYER_PATH,
    )
    if (
        not isinstance(char_id_list, str)
        and char_id_list == []
        or isinstance(char_id_list, str)
    ):
        return await convert_img(pic_500)

    img = await draw_enka_card(uid=uid, char_list=char_id_list, showfrom=1)
    return img, char_id_list


async def draw_enka_card(uid: str, char_list: List, showfrom: int = 0):
    char_data_list = []
    if 1102 in char_list:
        char_list.remove(1102)
        char_list.append(1102)
    for char in char_list:
        avatarName = avatarId2Name[str(char)]
        char_data_list.append(
            {
                'avatarName': avatarName,
                'avatarId': str(char),
            }
        )
    if showfrom == 0:
        line1 = f'展柜内有 {len(char_data_list)} 个角色!'
    elif char_data_list is None:
        return await convert_img(Image.new('RGBA', (0, 1), (255, 255, 255)))
    else:
        line1 = f'UID {uid} 刷新成功'
    line2 = f'可以使用 sr查询{char_data_list[0]["avatarName"]} 查询详情角色面板'
    char_num = len(char_data_list)
    if char_num <= 4:
        based_w, based_h = 1380, 926
        show_type = 1
    else:
        show_type = 0
        based_w, based_h = 1380, 310 + (((char_num - 1) // 4) + 1) * 320

    img = Image.open(TEXT_PATH / 'shin.jpg')
    img = crop_center_img(img, based_w, based_h)
    img.paste(tag, (0, 0), tag)

    img_draw = ImageDraw.Draw(img, 'RGBA')

    # 写底层文字
    img_draw.text(
        (690, based_h - 26),
        '--Created by qwerdvd-Designed By Wuyi-Thank for mihomo.me--',
        (22, 22, 22),
        fw_font_28,
        'mm',
    )

    img_draw.text(
        (225, 120),
        line1,
        white_color,
        sr_font_58,
        'lm',
    )
    img_draw.text(
        (225, 175),
        line2,
        gray_color,
        sr_font_24,
        'lm',
    )
    tasks = []
    for index, char_data in enumerate(char_data_list):
        if show_type == 0:
            tasks.append(draw_enka_char(index, img, char_data))
        else:
            tasks.append(draw_mihomo_char(index, img, char_data))
    await asyncio.gather(*tasks)
    return await convert_img(img)


async def draw_mihomo_char(index: int, img: Image.Image, char_data: Dict):
    char_id = char_data['avatarId']
    char_name = char_data['avatarName']
    char_star = await avatar_id_to_char_star(str(char_id))
    char_card = Image.open(TEXT_PATH / f'char{char_star}_bg.png')
    char_temp = Image.new('RGBA', (300, 650))
    char_img = (
        Image.open(str(CHAR_PREVIEW_PATH / f'{char_id}.png'))
        .convert('RGBA')
        .resize((449, 615))
    )
    if char_name == '希儿':
        char_img = char_img.resize((449, 650))
        char_img = char_img.crop((135, 0, 379, 457))
        char_temp.paste(char_img, (32, 98), char_img)
    else:
        char_img = char_img.crop((103, 0, 347, 517))
        char_temp.paste(char_img, (32, 38), char_img)
    char_card.paste(char_temp, (0, 0), char_bg_mask)

    img_draw = ImageDraw.Draw(char_card, 'RGBA')
    img_draw.text(
        (150, 585),
        char_name,
        white_color,
        sr_font_30,
        'mm',
    )
    x = 42 + index * 325
    img.paste(char_card, (x, 199), char_card)


async def draw_enka_char(index: int, img: Image.Image, char_data: Dict):
    char_id = char_data['avatarId']
    char_star = await avatar_id_to_char_star(str(char_id))
    char_card = Image.open(TEXT_PATH / f'ring_{char_star}.png')
    _path = CHAR_PREVIEW_PATH / f'{char_id}.png'
    char_img = Image.open(_path).convert('RGBA')
    char_img = char_img.resize(
        (int(char_img.size[0] * 0.76), int(char_img.size[1] * 0.76))
    )

    char_temp = Image.new('RGBA', (300, 400))
    card_temp = Image.new('RGBA', (300, 400))
    char_temp.paste(char_img, (19, 57), char_img)
    card_temp.paste(char_temp, (0, 0), char_mask)

    char_draw = ImageDraw.Draw(card_temp)
    char_draw.text(
        (144, 285),
        char_data['avatarName'],
        'white',
        sr_font_30,
        'mm',
    )

    img.paste(
        char_card,
        (113 + (index % 4) * 289, 152 + (index // 4) * 336),
        char_card,
    )

    img.paste(
        card_temp,
        (113 + (index % 4) * 289, 152 + (index // 4) * 336),
        card_temp,
    )
