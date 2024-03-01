import asyncio
from pathlib import Path
from typing import Dict, List, Union, Optional

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.utils.error_reply import get_error
from gsuid_core.utils.image.image_tools import (
    get_qq_avatar,
    draw_pic_with_ring,
)

from ..utils.mys_api import mys_api
from .utils import get_icon, wrap_list
from ..utils.image.convert import convert_img
from ..utils.fonts.first_world import fw_font_24
from ..sruid_utils.api.mys.models import (
    Stats,
    AvatarDetail,
    RoleBasicInfo,
    AvatarListItem,
    AvatarListItemDetail,
)
from ..utils.fonts.starrail_fonts import (
    sr_font_22,
    sr_font_24,
    sr_font_28,
    sr_font_30,
    sr_font_36,
)

TEXT_PATH = Path(__file__).parent / 'texture2D'

bg1 = Image.open(TEXT_PATH / 'bg1.png')
bg2 = Image.open(TEXT_PATH / 'bg2.png')
bg3 = Image.open(TEXT_PATH / 'bg3.png')
user_avatar = (
    Image.open(TEXT_PATH / '200101.png').resize((220, 220)).convert('RGBA')
)
char_bg_4 = Image.open(TEXT_PATH / 'rarity4_bg.png').convert('RGBA')
char_bg_5 = Image.open(TEXT_PATH / 'rarity5_bg.png').convert('RGBA')
circle = Image.open(TEXT_PATH / 'char_weapon_bg.png').convert('RGBA')
bg_img = Image.open(TEXT_PATH / 'bg_light.jpg')
rank_bg = Image.open(TEXT_PATH / 'rank_bg.png').convert('RGBA')
bg_color = (248, 248, 248)
white_color = (255, 255, 255)
color_color = (40, 18, 7)
first_color = (22, 8, 31)

elements = {
    'ice': Image.open(TEXT_PATH / 'IconNatureColorIce.png').convert('RGBA'),
    'fire': Image.open(TEXT_PATH / 'IconNatureColorFire.png').convert('RGBA'),
    'imaginary': Image.open(
        TEXT_PATH / 'IconNatureColorImaginary.png'
    ).convert('RGBA'),
    'quantum': Image.open(TEXT_PATH / 'IconNatureColorQuantum.png').convert(
        'RGBA'
    ),
    'lightning': Image.open(TEXT_PATH / 'IconNatureColorThunder.png').convert(
        'RGBA'
    ),
    'wind': Image.open(TEXT_PATH / 'IconNatureColorWind.png').convert('RGBA'),
    'physical': Image.open(TEXT_PATH / 'IconNaturePhysical.png').convert(
        'RGBA'
    ),
}


async def get_role_img(uid: str) -> Union[bytes, str]:
    return await draw_role_card(uid)


async def get_detail_img(qid: Union[str, int], uid: str, sender) -> Union[bytes, str]:
    return await get_detail_card(qid, uid, sender)


def _lv(level: int) -> str:
    return f'Lv.0{level}' if level < 10 else f'Lv.{level}'


async def _draw_card_1(
    sr_uid: str, role_basic_info: RoleBasicInfo, stats: Stats
) -> Image.Image:
    # 名称
    nickname = role_basic_info.nickname

    # 基本状态
    active_days = stats.active_days
    avater_num = stats.avatar_num
    achievement_num = stats.achievement_num
    chest_num = stats.chest_num
    level = role_basic_info.level

    # 忘却之庭
    abyss_process = stats.abyss_process

    img_bg1 = bg1.copy()
    bg1_draw = ImageDraw.Draw(img_bg1)

    # 写Nickname
    bg1_draw.text(
        (400, 85), nickname, font=sr_font_36, fill=white_color, anchor='mm'
    )
    # 写UID
    bg1_draw.text(
        (400, 165),
        f'UID {sr_uid}',
        font=sr_font_30,
        fill=white_color,
        anchor='mm',
    )
    # 贴头像
    img_bg1.paste(user_avatar, (286, 213), mask=user_avatar)

    # 写基本信息
    bg1_draw.text(
        (143, 590),
        str(active_days),
        font=sr_font_36,
        fill=white_color,
        anchor='mm',
    )  # 活跃天数
    bg1_draw.text(
        (270, 590),
        str(avater_num),
        font=sr_font_36,
        fill=white_color,
        anchor='mm',
    )  # 解锁角色
    bg1_draw.text(
        (398, 590),
        str(achievement_num),
        font=sr_font_36,
        fill=white_color,
        anchor='mm',
    )  # 达成成就
    bg1_draw.text(
        (525, 590),
        str(chest_num),
        font=sr_font_36,
        fill=white_color,
        anchor='mm',
    )  # 战利品开启
    bg1_draw.text(
        (666, 590), str(level), font=sr_font_36, fill=white_color, anchor='mm'
    )  # 开拓等级

    # 画忘却之庭
    bg1_draw.text(
        (471, 722),
        abyss_process,
        font=sr_font_30,
        fill=first_color,
        anchor='mm',
    )

    return img_bg1


async def _draw_avatar_card(
    avatar: AvatarListItem, equips: Dict[int, Optional[str]]
) -> Image.Image:
    char_bg = (char_bg_4 if avatar.rarity == 4 else char_bg_5).copy()
    char_draw = ImageDraw.Draw(char_bg)
    char_icon = (await get_icon(avatar.icon)).resize((110, 120))
    element_icon = elements[avatar.element]

    char_bg.paste(char_icon, (4, 8), mask=char_icon)
    char_bg.paste(element_icon, (10, 10), mask=element_icon)

    if avatar.rank > 0:
        char_bg.paste(rank_bg, (89, 6), mask=rank_bg)
        char_draw.text(
            (100, 21),
            f'{avatar.rank}',
            font=sr_font_22,
            fill=white_color,
            anchor='mm',
        )

    if equip := equips[avatar.id]:
        char_bg.paste(circle, (0, 0), mask=circle)
        equip_icon = (await get_icon(equip)).resize((48, 48))
        char_bg.paste(equip_icon, (9, 80), mask=equip_icon)

    char_draw.text(
        (60, 146),
        _lv(avatar.level),
        font=sr_font_24,
        fill=color_color,
        anchor='mm',
    )
    return char_bg


async def _draw_line(
    avatars: List[AvatarListItem], equips: Dict[int, Optional[str]]
) -> Image.Image:
    line = bg2.copy()
    x = 70
    char_bgs: List[Image.Image] = await asyncio.gather(
        *[_draw_avatar_card(avatar, equips) for avatar in avatars]
    )
    for char_bg in char_bgs:
        line.paste(char_bg, (x, 0), mask=char_bg)
        x += 135
    return line


async def _draw_card_2(
    avatars: List[AvatarListItem], equips: Dict[int, Optional[str]]
) -> Image.Image:
    # 角色部分 每五个一组
    lines = await asyncio.gather(
        *[
            _draw_line(five_avatars, equips)
            for five_avatars in wrap_list(avatars, 5)
        ]
    )
    img_card_2 = Image.new('RGBA', (800, len(lines) * 200))

    y = 0
    for line in lines:
        img_card_2.paste(line, (0, y), mask=line)
        y += 200
    return img_card_2


async def draw_role_card(sr_uid: str) -> Union[bytes, str]:
    role_index = await mys_api.get_role_index(sr_uid)
    # deal with hoyolab with no nickname and level api
    if int(str(sr_uid)[0]) < 6:
        role_basic_info = await mys_api.get_role_basic_info(sr_uid)
        if isinstance(role_basic_info, int):
            return get_error(role_basic_info)
    else:
        role_basic_info = {}
        role_basic_info['nickname'] = '开拓者'
        role_basic_info['level'] = 0

    if isinstance(role_index, int):
        return get_error(role_index)

    stats = role_index.stats
    avatars = role_index.avatar_list

    detail = await mys_api.get_avatar_info(sr_uid, avatars[0].id)
    if isinstance(detail, int):
        return get_error(detail)

    # 角色武器
    details = detail.avatar_list
    equips: Dict[int, Optional[str]] = {}
    for detail in details:
        equip = detail.equip
        equips[detail.id] = equip.icon if equip is not None else None

    # 绘制总图
    img1, img2 = await asyncio.gather(
        *[
            _draw_card_1(sr_uid, role_basic_info, stats),  # type: ignore
            _draw_card_2(avatars, equips),
        ]
    )
    img2: Image.Image
    height = img2.size[1]
    img = Image.new('RGBA', (800, 880 + height), bg_color)
    img.paste(img1, (0, 0))
    img.paste(img2, (0, 810))
    img.paste(bg3, (0, height + 810))
    return await convert_img(img)


async def _draw_detail_card(
    avatar_detail: AvatarDetail,
    avatar: AvatarListItemDetail,
    index: int,
    char_info: Image.Image,
) -> Image.Image:
    if str(avatar.rarity) == '5':
        avatar_img = Image.open(TEXT_PATH / 'bar_5.png')
    else:
        avatar_img = Image.open(TEXT_PATH / 'bar_4.png')
    avatar_draw = ImageDraw.Draw(avatar_img)
    char_icon = (await get_icon(avatar.icon)).resize((40, 40))
    element_icon = elements[avatar.element]
    avatar_img.paste(char_icon, (75, 10), mask=char_icon)
    avatar_draw.text(
        (130, 30),
        f'{avatar.name}',
        first_color,
        sr_font_24,
        'lm',
    )
    avatar_img.paste(element_icon, (270, 10), mask=element_icon)

    avatar_draw.text(
        (339, 30),
        f'{avatar.level}',
        first_color,
        sr_font_24,
        'mm',
    )

    avatar_draw.text(
        (385, 30),
        f'{avatar.rank}',
        first_color,
        sr_font_24,
        'mm',
    )

    avatar_draw.text(
        (429, 30),
        f'{avatar_detail.skills[0].cur_level}',
        first_color,
        sr_font_24,
        'mm',
    )

    avatar_draw.text(
        (469, 30),
        f'{avatar_detail.skills[1].cur_level}',
        first_color,
        sr_font_24,
        'mm',
    )

    avatar_draw.text(
        (515, 30),
        f'{avatar_detail.skills[2].cur_level}',
        first_color,
        sr_font_24,
        'mm',
    )

    avatar_draw.text(
        (553, 30),
        f'{avatar_detail.skills[3].cur_level}',
        first_color,
        sr_font_24,
        'mm',
    )

    if avatar.equip:
        equip_icon = (await get_icon(avatar.equip.icon)).resize((50, 50))
        avatar_img.paste(equip_icon, (595, 5), mask=equip_icon)

        avatar_draw.text(
            (680, 30),
            f'{avatar.equip.rank}',
            first_color,
            sr_font_24,
            'mm',
        )

        avatar_draw.text(
            (734, 30),
            f'Lv.{avatar.equip.level}',
            first_color,
            sr_font_24,
            'lm',
        )

        avatar_draw.text(
            (804, 30),
            f'{avatar.equip.name}',
            first_color,
            sr_font_24,
            'lm',
        )

    char_info.paste(avatar_img, (0, 585 + 62 * index), mask=avatar_img)

    return char_info


async def get_detail_card(
    qid: Union[str, int], sr_uid: str, sender
) -> Union[bytes, str]:
    # 获取角色列表
    avatar_list = await mys_api.get_avatar_info(sr_uid, 1001)
    if isinstance(avatar_list, int):
        return get_error(avatar_list)
    avatar_num = len(avatar_list.avatar_list)
    img_height = 663 + avatar_num * 62
    char_info = bg_img.copy()
    if img_height < 2300:
        char_info = char_info.crop((0, 0, 1050, img_height))
    else:
        char_info = char_info.resize((1050, img_height))
    char_img_draw = ImageDraw.Draw(char_info)

    char_title = Image.open(TEXT_PATH / 'title.png')
    char_info.paste(char_title, (0, 0), char_title)

    # 获取头像
    _id = str(qid)
    if _id.startswith('http'):
        char_pic = await get_qq_avatar(avatar_url=_id)
    elif sender.get('avatar') is not None:
        char_pic = await get_qq_avatar(avatar_url=sender['avatar'])
    else:
        char_pic = await get_qq_avatar(qid=qid)
    char_pic = await draw_pic_with_ring(char_pic, 250, None, False)

    char_info.paste(char_pic, (400, 88), char_pic)

    # 绘制抬头
    char_img_draw.text(
        (525, 420), f'UID {sr_uid}', white_color, sr_font_28, 'mm'
    )

    title_img = Image.open(TEXT_PATH / 'bar_title.png')
    char_info.paste(title_img, (0, 515), mask=title_img)

    for index, avatar in enumerate(avatar_list.avatar_list):
        avatar_detail = await mys_api.get_avatar_detail(sr_uid, str(avatar.id))
        if isinstance(avatar_detail, int):
            return get_error(avatar_detail)
        # 200
        char_info = await _draw_detail_card(
            avatar_detail,
            avatar,
            index,
            char_info,
        )

    # 写底层文字
    char_img_draw.text(
        (525, img_height - 45),
        '--SR skill statistics by StarrailUID & Code by jiluoQAQ & Power by GsCore--',
        (255, 255, 255),
        fw_font_24,
        'mm',
    )

    res = await convert_img(char_info)
    logger.info('[查询练度统计]绘图已完成,等待发送!')
    return res
