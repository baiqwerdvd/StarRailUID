from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw
from gsuid_core.logger import logger

from ..utils.mys_api import mys_api
from ..utils.error_reply import get_error
from ..utils.image.convert import convert_img
from ..utils.fonts.starrail_fonts import sr_font_20, sr_font_28, sr_font_34

TEXT_PATH = Path(__file__).parent / 'texture2d'

monthly_bg = Image.open(TEXT_PATH / 'monthly_bg.png')
avatar_default = Image.open(TEXT_PATH / '200101.png')

first_color = (29, 29, 29)
second_color = (67, 61, 56)
second_color2 = (98, 98, 98)
black_color = (54, 54, 54)

COLOR_MAP = {
    '每日活跃': (248, 227, 157),
    '活动奖励': (99, 231, 176),
    '冒险奖励': (114, 205, 251),
    '模拟宇宙奖励': (160, 149, 248),
    '忘却之庭奖励': (221, 119, 250),
    '邮件奖励': (244, 110, 104),
    '其他': (255, 242, 200),
    'Daily Activity': (248, 227, 157),
    'Events': (99, 231, 176),
    'Adventure': (114, 205, 251),
    'moni': (160, 149, 248),
    'Spiral Abyss': (221, 119, 250),
    'Quests': (244, 110, 104),
    'Other': (255, 242, 200),
}


async def draw_note_img(sr_uid: str) -> Union[bytes, str]:
    # 获取数据
    data = await mys_api.get_award(sr_uid)
    if isinstance(data, int):
        return get_error(data)
    # nickname and level
    role_basic_info = await mys_api.get_role_basic_info(sr_uid)
    if isinstance(role_basic_info, int):
        return get_error(role_basic_info)
    nickname = role_basic_info['nickname']

    day_hcoin = data['day_data']['current_hcoin']
    day_rails_pass = data['day_data']['current_rails_pass']
    lastday_hcoin = 0
    lastday_rails_pass = 0
    if int(sr_uid[0]) < 6:
        lastday_hcoin = data['day_data']['last_hcoin']
        lastday_rails_pass = data['day_data']['last_rails_pass']
    month_hcoin = data['month_data']['current_hcoin']
    month_rails_pass = data['month_data']['current_rails_pass']
    lastmonth_hcoin = data['month_data']['last_hcoin']
    # lastmonth_rails_pass = data['month_data']['last_rails_pass']

    day_hcoin_str = await int_carry(day_hcoin)
    # day_rails_pass_str = await int_carry(day_rails_pass)
    # month_hcoin_str = await int_carry(month_hcoin)
    # month_rails_pass_str = await int_carry(month_rails_pass)
    # lastday_stone_str = f'昨日星琼:{await int_carry(lastday_hcoin)}'
    # lastday_mora_str = f'昨日星轨通票&星轨专票:' \
    #                    f'{await int_carry(lastday_rails_pass)}'
    # lastmonth_stone_str = f'上月星琼:{await int_carry(lastmonth_hcoin)}'
    # lastmonth_mora_str = f'上月星轨通票&星轨专票:' \
    #                      f'{await int_carry(lastmonth_rails_pass)}'

    # 处理数据
    # 今日比昨日 星琼
    day_hcoin_percent = day_hcoin / lastday_hcoin if lastday_hcoin != 0 else 1
    day_hcoin_percent = day_hcoin_percent if day_hcoin_percent <= 1 else 1
    # 今日比昨日 星轨通票&星轨专票
    day_rails_pass_percent = (
        day_rails_pass / lastday_rails_pass if lastday_rails_pass != 0 else 1
    )
    day_rails_pass_percent = (
        day_rails_pass_percent if day_rails_pass_percent <= 1 else 1
    )
    # 本月比上月 星琼
    month_hcoin_percent = (
        month_hcoin / lastmonth_hcoin if lastmonth_hcoin != 0 else 1
    )
    month_hcoin_percent = (
        month_hcoin_percent if month_hcoin_percent <= 1 else 1
    )
    # 本月比上月 星轨通票&星轨专票
    month_rails_pass_percent = (
        month_rails_pass / month_rails_pass if month_rails_pass != 0 else 1
    )
    month_rails_pass_percent = (
        month_rails_pass_percent if month_rails_pass_percent <= 1 else 1
    )

    # # 获取背景图片各项参数
    # based_w = 700
    # based_h = 1300

    img = monthly_bg.copy()
    avatar_img = avatar_default.copy()
    char_pic = avatar_img.convert('RGBA').resize(
        (125, 125), Image.Resampling.LANCZOS  # type: ignore
    )
    img.paste(char_pic, (115, 133), char_pic)
    img_draw = ImageDraw.Draw(img)

    # 写Nickname
    img_draw.text(
        (310, 183), nickname, font=sr_font_34, fill=first_color, anchor='lm'
    )

    # 写UID
    img_draw.text(
        (300, 215),
        f'UID {sr_uid}',
        font=sr_font_20,
        fill=second_color2,
        anchor='lm',
    )

    # 写本日星琼
    img_draw.text(
        (300, 260),
        day_hcoin_str,
        font=sr_font_28,
        fill=second_color2,
        anchor='lm',
    )

    # 写本月星琼
    img_draw.text(
        (300, 260),
        day_hcoin_str,
        font=sr_font_28,
        fill=second_color2,
        anchor='lm',
    )

    # 写本日星琼
    img_draw.text(
        (300, 260),
        day_hcoin_str,
        font=sr_font_28,
        fill=second_color2,
        anchor='lm',
    )

    # 写本日星琼
    img_draw.text(
        (300, 260),
        day_hcoin_str,
        font=sr_font_28,
        fill=second_color2,
        anchor='lm',
    )

    ring_pic = Image.open(TEXT_PATH / 'ring.apng')
    ring_list = []
    ring_list.append([int(day_hcoin_percent * 89 + 0.5), (-5, 475)])
    ring_list.append([int(day_rails_pass_percent * 89 + 0.5), (371, 475)])
    ring_list.append([int(month_hcoin_percent * 89 + 0.5), (-5, 948)])
    ring_list.append([int(month_rails_pass_percent * 89 + 0.5), (371, 948)])
    ring_list.sort(key=lambda x: -x[0], reverse=True)
    print(ring_list)
    for i in ring_list:
        ring_pic.seek(i[0])
        img.paste(ring_pic, i[1], ring_pic)

    # 具体数据
    # img_draw.text((243, 718), str(day_hcoin_percent),
    # first_color, sr_font_58, 'mm')
    # img_draw.text((625, 718), str(day_rails_pass_percent),
    # first_color, sr_font_58, 'mm')
    # img_draw.text((245, 1192), str(month_hcoin_str),
    # first_color, sr_font_58, 'mm')
    # img_draw.text((621, 1192), str(month_rails_pass_str),
    # first_color, sr_font_58, 'mm')
    #
    # img_draw.text(
    #     (245, 923), lastday_stone_str, second_color, sr_font_26, 'mm'
    # )
    # img_draw.text(
    #     (621, 923), lastday_mora_str, second_color, sr_font_26, 'mm'
    # )
    # img_draw.text(
    #     (245, 1396), lastmonth_stone_str, second_color, sr_font_26, 'mm'
    # )
    # img_draw.text(
    #     (621, 1396), lastmonth_mora_str, second_color, sr_font_26, 'mm'
    # )

    if data['month_data']['group_by'] == []:
        for index, action in enumerate(COLOR_MAP):
            if action == '其他':
                continue
    else:
        xy = ((139, 579), (347, 787))
        temp = -90
        for index, i in enumerate(data['month_data']['group_by']):
            img_draw.pieslice(
                xy,
                temp,
                temp + (i['percent'] / 100) * 360,
                COLOR_MAP[i['action_name']],
            )
            temp = temp + (i['percent'] / 100) * 360
            if i['action'] == '其他':
                continue
            img_draw.rectangle(
                ((407, 1523 + index * 52), (453, 1548 + index * 52)),
                fill=COLOR_MAP[i['action_name']],
            )

    img = await convert_img(img)
    logger.info('[开拓月历] 图片绘制完成!等待发送...')
    return img


async def int_carry(i: int) -> str:
    if i >= 100000:
        i_str = '{:.1f}W'.format(i / 10000)
    else:
        i_str = str(i)
    return i_str
