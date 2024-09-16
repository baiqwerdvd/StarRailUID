import copy
import json
import math
from pathlib import Path
import textwrap
from typing import Dict, Union

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_text_by_line
from .to_data import api_to_dict

from ..sruid_utils.api.mihomo.models import Character, Relic, Skill, LightCone, Attribute, SubAffix
from ..utils.error_reply import CHAR_HINT
from ..utils.excel.read_excel import light_cone_ranks
from ..utils.fonts.first_world import fw_font_28
from ..utils.fonts.starrail_fonts import (
    sr_font_18,
    sr_font_20,
    sr_font_23,
    sr_font_24,
    sr_font_26,
    sr_font_28,
    sr_font_34,
    sr_font_38,
)
from ..utils.map.SR_MAP_PATH import (
    AvatarRelicScore,
    RelicId2Rarity,
    avatarId2Name,
)
from ..utils.map.name_covert import alias_to_char_name, name_to_avatar_id
from ..utils.resource.RESOURCE_PATH import (
    CHAR_PORTRAIT_PATH,
    PLAYER_PATH,
    RELIC_PATH,
    SKILL_PATH,
    WEAPON_PATH,
)

Excel_path = Path(__file__).parent
with Path.open(Excel_path / "Excel" / "SkillData.json", encoding="utf-8") as f:
    skill_dict = json.load(f)

TEXT_PATH = Path(__file__).parent / "texture2D"

bg_img = Image.open(TEXT_PATH / "bg.png")
white_color = (213, 213, 213)
NUM_MAP = {
    0: "零",
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
}

RANK_MAP = {
    1: "_rank1.png",
    2: "_rank2.png",
    3: "_ultimate.png",
    4: "_rank4.png",
    5: "_skill.png",
    6: "_rank6.png",
}

skill_type_map = {
    "Normal": ("普攻", "basic_atk"),
    "BPSkill": ("战技", "skill"),
    "Ultra": ("终结技", "ultimate"),
    "Talent": ("天赋", "talent"),
}

RELIC_POS = {
    "1": (26, 1162),
    "2": (367, 1162),
    "3": (700, 1162),
    "4": (26, 1593),
    "5": (367, 1593),
    "6": (700, 1593),
}

RELIC_CNT = {
    1: "",
    2: "●",
    3: "●●",
    4: "●●●",
    5: "●●●●",
    6: "●●●●●",
}


async def draw_char_img(char: Character, sr_uid: str, msg: str) -> Union[bytes, str]:
    damage_len = 0
    damage_list = []
    bg_height = 0
    if damage_len > 0:
        bg_height = 48 * (1 + damage_len) + 48
    char_change = 0
    msg_h = 0
    para = []
    if "换" in msg or "拿" in msg or "带" in msg:
        char_change = 1
        para = textwrap.wrap(msg, width=45)
        msg_h = 40 * (len(para) + 1)
        bg_height = bg_height + msg_h
    # 放角色立绘
    char_info = bg_img.copy()
    char_info = char_info.resize((1050, 2050 + bg_height))
    char_img = (
        Image.open(CHAR_PORTRAIT_PATH / f"{char.id}.png")
        .resize((1050, 1050))
        .convert("RGBA")
    )
    char_info.paste(char_img, (-220, -130), char_img)
    # 放属性图标
    attr_img = Image.open(TEXT_PATH / f"IconAttribute{char.element['id']}.png")
    char_info.paste(attr_img, (540, 122), attr_img)

    # 放角色名
    char_img_draw = ImageDraw.Draw(char_info)
    char_img_draw.text((620, 162), char.name, (255, 255, 255), sr_font_38, "lm")
    if hasattr(sr_font_38, "getsize"):
        char_name_len = sr_font_38.getsize(char.char_name)[0]  # type: ignore
    else:
        bbox = sr_font_38.getbbox(char.name)
        char_name_len = bbox[2] - bbox[0]

    # 放等级
    char_img_draw.text(
        (620 + char_name_len + 50, 168),
        f"LV.{char.level!s}",
        white_color,
        sr_font_24,
        "mm",
    )

    # 放星级
    rarity_img = Image.open(
        TEXT_PATH / f"LightCore_Rarity{char.rarity}.png"
    ).resize((306, 72))
    char_info.paste(rarity_img, (490, 189), rarity_img)

    # 放命座
    rank_img = Image.open(TEXT_PATH / "ImgNewBg.png")
    rank_img_draw = ImageDraw.Draw(rank_img)
    rank_img_draw.text(
        (70, 44), f"{NUM_MAP[char.rank]}命", white_color, sr_font_28, "mm"
    )
    char_info.paste(rank_img, (722, 181), rank_img)

    # 放uid
    char_img_draw.text(
        (995, 715),
        f"uid {sr_uid}",
        white_color,
        sr_font_28,
        "rm",
    )

    # 放属性列表
    attr_bg = Image.open(TEXT_PATH / "attr_bg.png")
    attr_bg_draw = ImageDraw.Draw(attr_bg)
    # 属性
    attr = {}
    # 遍历基础属性，获取对应的名称和值
    for attribute in char.attributes:
        attr[attribute['field']] = {
            'base': attribute['value'] or 0,
            'add': 0  # 防止副词条没有该属性时为None
        }
    # 添加占位
    # 效果命中
    attr['effect_hit'] = {
        'base': 0,
        'add': 0,
    }
    # 效果抵抗
    attr['effect_res'] = {
        'base': 0,
        'add': 0,
    }
    # 击破特攻
    attr['break_dmg'] = {
        'base': 0,
        'add': 0,
    }
    # 遍历属性加项，获取对应的名称和值
    for addition in char.additions:
        if addition['field'] not in attr:
            # 创建一个新的键，初始化 base 和 add 为默认值
            attr[addition['field']] = {'base': 0, 'add': 0}
        attr[addition['field']]['add'] = addition['value'] or 0

    # 生命值
    attr_bg_draw.text((413, 31), f"{round(attr['hp'].get('base') + attr['hp'].get('add'))}", white_color, sr_font_26,
                      "rm")
    attr_bg_draw.text(
        (428, 31),
        f"(+{round(attr['hp'].get('add'))!s})",
        (95, 251, 80),
        sr_font_26,
        anchor="lm",
    )
    # 攻击力
    attr_bg_draw.text(
        (413, 31 + 48),
        f"{round(attr['atk'].get('base') + attr['atk'].get('add'))}",
        white_color,
        sr_font_26,
        "rm",
    )
    attr_bg_draw.text(
        (428, 31 + 48),
        f"(+{round(attr['atk'].get('add'))!s})",
        (95, 251, 80),
        sr_font_26,
        anchor="lm",
    )
    # 防御力
    attr_bg_draw.text(
        (413, 31 + 48 * 2),
        f"{round(attr['def'].get('base') + attr['def'].get('add'))}",
        white_color,
        sr_font_26,
        "rm",
    )
    attr_bg_draw.text(
        (428, 31 + 48 * 2),
        f"(+{round(attr['def'].get('add'))!s})",
        (95, 251, 80),
        sr_font_26,
        anchor="lm",
    )
    # 速度
    attr_bg_draw.text(
        (413, 31 + 48 * 3),
        f"{round(attr['spd'].get('base') + attr['spd'].get('add'))}",
        white_color,
        sr_font_26,
        "rm",
    )
    attr_bg_draw.text(
        (428, 31 + 48 * 3),
        f"(+{round(attr['spd'].get('add'))!s})",
        (95, 251, 80),
        sr_font_26,
        anchor="lm",
    )
    # 暴击率
    crit_date = (attr['crit_rate'].get('base', 0) + attr['crit_rate'].get('add', 0)) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 4),
        f"{crit_date :.1f}",
        white_color,
        sr_font_26,
        "rm",
    )
    # 暴击伤害
    crit_dmg = (attr['crit_dmg'].get('base', 0) + attr['crit_dmg'].get('add', 0)) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 5),
        f"{crit_dmg :.1f}",
        white_color,
        sr_font_26,
        "rm",
    )
    # 效果命中
    effect_hit = attr['effect_hit'].get('add', 0) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 6),
        f"{effect_hit:.1f}%",
        white_color,
        sr_font_26,
        "rm",
    )
    # 效果抵抗
    effect_res = attr['effect_res'].get("add", 0) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 7),
        f"{effect_res:.1f}%",
        white_color,
        sr_font_26,
        "rm",
    )
    # 击破特攻
    break_dmg = attr['break_dmg'].get("add", 0) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 8),
        f"{break_dmg:.1f}%",
        white_color,
        sr_font_26,
        "rm",
    )
    char_info.paste(attr_bg, (475, 256), attr_bg)
    # 命座
    for rank in range(6):
        rank_bg = Image.open(TEXT_PATH / "mz_bg.png")
        rank_no_bg = Image.open(TEXT_PATH / "mz_no_bg.png")
        if rank < char.rank:
            rank_img = (
                Image.open(SKILL_PATH / f"{char.id}{RANK_MAP[rank + 1]}")
                .convert("RGBA")
                .resize((50, 50))
            )
            rank_bg.paste(rank_img, (19, 19), rank_img)
            char_info.paste(rank_bg, (20 + rank * 80, 630), rank_bg)
        else:
            rank_img = (
                Image.open(SKILL_PATH / f"{char.id}{RANK_MAP[rank + 1]}")
                .resize((50, 50))
                .convert("RGBA")
            )
            rank_img.putalpha(
                rank_img.getchannel("A").point(
                    lambda x: round(x * 0.45) if x > 0 else 0
                )
            )
            rank_no_bg.paste(rank_img, (19, 19), rank_img)
            char_info.paste(rank_no_bg, (20 + rank * 80, 630), rank_no_bg)

    # 技能
    skill_bg = Image.open(TEXT_PATH / "skill_bg.png")
    i = 0
    # 只显示前四个，因为其他的都是一级，显示意义不大
    # 另一个原因是第五个是dev_连携，意思是普攻进入战斗，不知道后期会是什么样子
    for skill in char.skills[:4]:
        # 转为类
        skill_data = Skill(**skill)
        skill_attr_img = Image.open(TEXT_PATH / f"skill_attr{i + 1}.png")
        skill_panel_img = Image.open(TEXT_PATH / "skill_panel.png")
        skill_img = (
            Image.open(
                SKILL_PATH / f'{char.id}_'
                             f'{skill_type_map[skill_data.type][1]}.png'
            )
            .convert("RGBA")
            .resize((55, 55))
        )
        skill_panel_img.paste(skill_img, (18, 15), skill_img)
        skill_panel_img.paste(skill_attr_img, (80, 10), skill_attr_img)
        skill_panel_img_draw = ImageDraw.Draw(skill_panel_img)
        skill_panel_img_draw.text(
            (108, 25),
            f'{skill_type_map[skill_data.type][0]}',
            white_color,
            sr_font_26,
            "lm",
        )
        skill_panel_img_draw.text(
            (89, 55),
            f'Lv.{skill_data.level}',
            white_color,
            sr_font_26,
            "lm",
        )
        skill_panel_img_draw.text(
            (75, 90),
            f'{skill_data.name}',
            (105, 105, 105),
            sr_font_20,
            "mm",
        )
        skill_bg.paste(skill_panel_img, (50 + 200 * i, 35), skill_panel_img)
        i += 1
    char_info.paste(skill_bg, (0, 710), skill_bg)

    # 光锥
    if char.light_cone != {}:
        # 转换为Class
        light_cone = LightCone(**char.light_cone)
        light_cone_bg = Image.open(TEXT_PATH / "weapon_bg.png")
        light_cone_id = light_cone.id
        light_cone_img = (
            Image.open(WEAPON_PATH / f"{light_cone_id}.png")
            .convert("RGBA")
            .resize((170, 180))
        )
        light_cone_bg.paste(light_cone_img, (20, 90), light_cone_img)
        weapon_bg_draw = ImageDraw.Draw(light_cone_bg)
        weapon_bg_draw.text(
            (345, 47),
            f'{light_cone.name}',
            white_color,
            sr_font_34,
            "lm",
        )
        if hasattr(sr_font_34, "getsize"):
            weapon_name_len = sr_font_34.getsize(  # type: ignore
                light_cone.name
            )[0]
        else:
            bbox = sr_font_34.getbbox(light_cone.name)
            weapon_name_len = bbox[2] - bbox[0]
        # 放阶
        rank_img = Image.open(TEXT_PATH / "ImgNewBg.png")
        rank_img_draw = ImageDraw.Draw(rank_img)
        rank_img_draw.text(
            (70, 44),
            f'{NUM_MAP[light_cone.rank]}阶',
            white_color,
            sr_font_28,
            "mm",
        )
        light_cone_bg.paste(rank_img, (weapon_name_len + 330, 2), rank_img)

        rarity_img = Image.open(
            TEXT_PATH / f'LightCore_Rarity{light_cone.rarity}.png'
        ).resize((306, 72))
        light_cone_bg.paste(rarity_img, (223, 55), rarity_img)
        weapon_bg_draw.text(
            (498, 90),
            f'Lv.{light_cone.level}',
            white_color,
            sr_font_28,
            "mm",
        )

        # 武器技能
        desc = light_cone_ranks[str(light_cone.id)]["desc"]
        desc_params = light_cone_ranks[str(light_cone.id)]["params"][
            light_cone.rank - 1
            ]
        for i in range(len(desc_params)):
            temp = math.floor(desc_params[i] * 1000) / 10
            desc = desc.replace(f"#{i + 1}[i]%", f"{temp!s}%")
            desc = desc.replace(f"#{i + 1}[f1]%", f"{temp!s}%")
        for i in range(len(desc_params)):
            desc = desc.replace(f"#{i + 1}[i]", str(desc_params[i]))
        desclist = desc.split()
        desctexty = 115
        for desctext in desclist:
            desctexty = draw_text_by_line(
                light_cone_bg,
                (210, desctexty),  # type: ignore
                desctext,
                sr_font_24,
                "#F9F9F9",
                370,
            )
            desctexty += 28
        char_info.paste(light_cone_bg, (0, 855), light_cone_bg)
    else:
        char_img_draw.text(
            (525, 1005),
            "No light cone!",
            white_color,
            fw_font_28,
            "mm",
        )

    # 遗器
    if char.relics:
        weapon_rank_bg = Image.open(TEXT_PATH / "rank_bg.png")
        char_info.paste(weapon_rank_bg, (735, 880), weapon_rank_bg)
        relic_score = 0
        for relic in char.relics:
            relic_data = Relic(**relic)
            rarity = RelicId2Rarity[str(relic_data.id)]
            relic_img = Image.open(TEXT_PATH / f"yq_bg{rarity}.png")
            if str(relic_data.set_id)[0] == "3":
                relic_piece_img = Image.open(
                    RELIC_PATH / f'{relic_data.set_id}_{relic_data.type - 5}.png'
                )
            else:
                relic_piece_img = Image.open(
                    RELIC_PATH / f'{relic_data.set_id}_{relic_data.type - 1}.png'
                )
            relic_piece_new_img = relic_piece_img.resize(
                (105, 105), Image.Resampling.LANCZOS
            ).convert("RGBA")
            relic_img.paste(
                relic_piece_new_img,
                (200, 90),
                relic_piece_new_img,
            )
            rarity_img = Image.open(
                TEXT_PATH / f'LightCore_Rarity'
                            f'{RelicId2Rarity[str(relic_data.id)]}.png'
            ).resize((200, 48))
            relic_img.paste(rarity_img, (-10, 80), rarity_img)
            relic_img_draw = ImageDraw.Draw(relic_img)
            if len(relic_data.name) <= 5:
                main_name = relic_data.name
            else:
                main_name = relic_data.name[:2] + relic_data.name[4:]
            relic_img_draw.text(
                (30, 70),
                main_name,
                (255, 255, 255),
                sr_font_34,
                anchor="lm",
            )

            # 主属性
            main_value = relic_data.main_affix['value']
            main_name: str = relic_data.main_affix['name']
            main_level: int = relic_data.level

            if main_name in ["攻击力", "生命值", "防御力", "速度"]:
                mainValueStr = f"{main_value:.1f}"
            else:
                mainValueStr = str(math.floor(main_value * 1000) / 10) + "%"

            mainNameNew = (
                main_name.replace("百分比", "")
                .replace("伤害加成", "伤加成")
                .replace("属性伤害", "伤害")
            )

            relic_img_draw.text(
                (35, 150),
                mainNameNew,
                (255, 255, 255),
                sr_font_28,
                anchor="lm",
            )
            relic_img_draw.text(
                (35, 195),
                f"+{mainValueStr}",
                (255, 255, 255),
                sr_font_28,
                anchor="lm",
            )
            relic_img_draw.text(
                (180, 105),
                f"+{main_level!s}",
                (255, 255, 255),
                sr_font_23,
                anchor="mm",
            )

            single_relic_score = 0
            main_value_score = await get_relic_score(
                relic_data.main_affix['type'],
                main_value,
                char.name,
                True,
                relic_data.type,
            )
            single_relic_score += main_value_score
            for index, i in enumerate(relic_data.sub_affix):
                # 转换为class
                sub_affix = SubAffix(**i)
                subName: str = sub_affix.name
                subCnt = sub_affix.count
                subValue = sub_affix.value
                subProperty = sub_affix.type
                tmp_score = await get_relic_score(
                    subProperty, subValue, char.name, False, relic_data.type
                )
                single_relic_score += tmp_score

                if subName in ["攻击力", "生命值", "防御力", "速度"]:
                    subValueStr = f"{subValue:.1f}"
                else:
                    subValueStr = f"{subValue * 100:.1f}" + "%"
                subNameStr = subName.replace("百分比", "").replace("元素", "")
                # 副词条文字颜色
                if tmp_score == 0:
                    relic_color = (150, 150, 150)
                else:
                    relic_color = (255, 255, 255)

                relic_img_draw.text(
                    (47, 237 + index * 47),
                    f"{subNameStr}",
                    relic_color,
                    sr_font_26,
                    anchor="lm",
                )
                relic_img_draw.text(
                    (155, 237 + index * 47),
                    f"{RELIC_CNT[subCnt]}",
                    relic_color,
                    sr_font_18,
                    anchor="lm",
                )
                relic_img_draw.text(
                    (290, 237 + index * 47),
                    f"{subValueStr}",
                    relic_color,
                    sr_font_26,
                    anchor="rm",
                )
            relic_img_draw.text(
                (210, 195),
                f"{int(single_relic_score)}分",
                (255, 255, 255),
                sr_font_28,
                anchor="rm",
            )

            char_info.paste(relic_img, RELIC_POS[str(relic_data.type)], relic_img)
            relic_score += single_relic_score
        if relic_score > 210:
            relic_value_level = Image.open(TEXT_PATH / "CommonIconSSS.png")
            char_info.paste(relic_value_level, (825, 963), relic_value_level)
        elif relic_score > 190:
            relic_value_level = Image.open(TEXT_PATH / "CommonIconSS.png")
            char_info.paste(relic_value_level, (825, 963), relic_value_level)
        elif relic_score > 160:
            relic_value_level = Image.open(TEXT_PATH / "CommonIconS.png")
            char_info.paste(relic_value_level, (825, 963), relic_value_level)
        elif relic_score > 130:
            relic_value_level = Image.open(TEXT_PATH / "CommonIconA.png")
            char_info.paste(relic_value_level, (825, 963), relic_value_level)
        elif relic_score > 80:
            relic_value_level = Image.open(TEXT_PATH / "CommonIconB.png")
            char_info.paste(relic_value_level, (825, 963), relic_value_level)
        elif relic_score > 0:
            relic_value_level = Image.open(TEXT_PATH / "CommonIconC.png")
            char_info.paste(relic_value_level, (825, 963), relic_value_level)

    else:
        char_img_draw.text(
            (525, 1565),
            "未装备",
            white_color,
            fw_font_28,
            "mm",
        )

    if damage_len > 0:
        damage_title_img = Image.open(TEXT_PATH / "base_info_pure.png")
        char_info.paste(damage_title_img, (0, 2028), damage_title_img)
        # 写伤害
        char_img_draw.text(
            (55, 2048),
            "角色动作",
            white_color,
            sr_font_26,
            "lm",
        )

        char_img_draw.text(
            (370, 2048),
            "暴击值",
            white_color,
            sr_font_26,
            "lm",
        )

        char_img_draw.text(
            (560, 2048),
            "期望值",
            white_color,
            sr_font_26,
            "lm",
        )

        char_img_draw.text(
            (750, 2048),
            "满配辅助末日兽",
            white_color,
            sr_font_26,
            "lm",
        )
        damage_num = 0
        for damage_info in damage_list:
            damage_num = damage_num + 1
            if damage_num % 2 == 0:
                damage_img = Image.open(TEXT_PATH / "attack_1.png")
            else:
                damage_img = Image.open(TEXT_PATH / "attack_2.png")
            char_info.paste(damage_img, (0, 2028 + damage_num * 48), damage_img)
            char_img_draw.text(
                (55, 2048 + damage_num * 48),
                f'{damage_info["name"]}',
                white_color,
                sr_font_26,
                "lm",
            )
            dmg_list = damage_info["damagelist"]
            if len(dmg_list) == 3:
                damage1 = math.floor(dmg_list[0])  # type: ignore
                char_img_draw.text(
                    (370, 2048 + damage_num * 48),
                    f"{damage1}",
                    white_color,
                    sr_font_26,
                    "lm",
                )
                damage2 = math.floor(dmg_list[1])  # type: ignore
                char_img_draw.text(
                    (560, 2048 + damage_num * 48),
                    f"{damage2}",
                    white_color,
                    sr_font_26,
                    "lm",
                )
                damage3 = math.floor(dmg_list[2])  # type: ignore
                char_img_draw.text(
                    (750, 2048 + damage_num * 48),
                    f"{damage3}",
                    white_color,
                    sr_font_26,
                    "lm",
                )
            else:
                damage = math.floor(dmg_list[0])  # type: ignore
                char_img_draw.text(
                    (560, 2048 + damage_num * 48),
                    f"{damage}",
                    white_color,
                    sr_font_26,
                    "lm",
                )

    if char_change == 1:
        char_img_draw.text(
            (525, 2022 + bg_height - msg_h),
            "面板数据来源于: 【面板替换】",
            (180, 180, 180),
            sr_font_26,
            "mm",
        )

        current_h = 2022 + bg_height - msg_h + 40
        for line in para:
            char_img_draw.text(
                (525, current_h),
                line,
                (180, 180, 180),
                sr_font_26,
                "mm",
            )
            current_h += 35

    # 写底层文字
    char_img_draw.text(
        (525, 2022 + bg_height),
        "--Created by qwerdvd-Designed By Wuyi-Thank for mihomo.me--",
        (255, 255, 255),
        sr_font_28,
        "mm",
    )

    # 发送图片
    res = await convert_img(char_info)
    logger.info("[sr面板]绘图已完成,等待发送!")
    return res


async def get_char_data(
    uid: str, char_name: str, enable_self: bool = True
) -> Union[Dict, str]:
    player_path = PLAYER_PATH / str(uid)
    SELF_PATH = player_path / "SELF"
    if "开拓者" in str(char_name):
        char_name = "开拓者"
    char_id = await name_to_avatar_id(char_name)
    if char_id == "":
        char_name = await alias_to_char_name(char_name)
    if char_name is False:
        return "请输入正确的角色名"
    char_path = player_path / f"{char_name}.json"
    char_self_path = SELF_PATH / f"{char_name}.json"
    path = Path()
    if char_path.exists():
        path = char_path
    elif enable_self and char_self_path.exists():
        path = char_self_path
    else:
        char_id_list, _ = await api_to_dict(uid, save_path=PLAYER_PATH)
        charname_list = []
        if isinstance(char_id_list, str):
            return char_id_list
        for char in char_id_list:
            charname = avatarId2Name[str(char)]
            charname_list.append(charname)
        if str(char_name) in charname_list:
            if char_path.exists():
                path = char_path
            elif enable_self and char_self_path.exists():
                path = char_self_path
        else:
            return CHAR_HINT.format(char_name, char_name)

    with Path.open(path, encoding="utf8") as fp:
        return json.load(fp)


async def get_relic_score(
    subProperty: str, subValue, char_name: str, is_main: bool, relicType: int
) -> float:
    relic_score = 0
    weight_dict = {}
    for item in AvatarRelicScore:
        if item["role"] == char_name:
            weight_dict = item
    if weight_dict == {}:
        return 0
    if is_main:
        elementlist = [
            "Quantum",
            "Thunder",
            "Wind",
            "Physical",
            "Imaginary",
            "Ice",
            "Fire",
        ]
        if relicType in [3, 4, 5, 6]:
            if subProperty.__contains__("AddedRatio") and relicType == 5:
                if subProperty.split("AddedRatio")[0] in elementlist:
                    subProperty = "AttributeAddedRatio"
            if weight_dict.get(subProperty, 0) > 0:
                relic_score += 5.83
    else:
        if subProperty == "CriticalDamageBase":
            add_value = subValue * 1 * weight_dict["CriticalDamageBase"] * 100
            relic_score += add_value
        if subProperty == "CriticalChanceBase":
            add_value = subValue * 2 * weight_dict["CriticalChanceBase"] * 100
            relic_score += add_value
        if subProperty == "AttackDelta":
            add_value = subValue * 0.3 * 0.5 * weight_dict["AttackDelta"] * 1.0
            relic_score += add_value
        if subProperty == "DefenceDelta":
            add_value = subValue * 0.3 * 0.5 * weight_dict["DefenceDelta"] * 1.0
            relic_score += add_value
        if subProperty == "HPDelta":
            add_value = subValue * 0.158 * 0.5 * weight_dict["HPDelta"] * 1.0
            relic_score += add_value
        if subProperty == "AttackAddedRatio":
            add_value = subValue * 1.5 * weight_dict["AttackAddedRatio"] * 100
            relic_score += add_value
        if subProperty == "DefenceAddedRatio":
            add_value = subValue * 1.19 * weight_dict["DefenceAddedRatio"] * 100
            relic_score += add_value
        if subProperty == "HPAddedRatio":
            add_value = subValue * 1.5 * weight_dict["HPAddedRatio"] * 100
            relic_score += add_value
        if subProperty == "SpeedDelta":
            add_value = subValue * 2.53 * weight_dict["SpeedDelta"]
            relic_score += add_value
        if subProperty == "BreakDamageAddedRatioBase":
            add_value = subValue * 1.0 * weight_dict["BreakDamageAddedRatioBase"] * 100
            relic_score += add_value
        if subProperty == "StatusProbabilityBase":
            add_value = subValue * 1.49 * weight_dict["StatusProbabilityBase"] * 100
            relic_score += add_value
        if subProperty == "StatusResistanceBase":
            add_value = subValue * 1.49 * weight_dict["StatusResistanceBase"] * 100
            relic_score += add_value
    return relic_score
