import copy
import json
import math
import textwrap
from pathlib import Path
from typing import Dict, Union

from PIL import Image, ImageDraw
from gsuid_core.logger import logger
from starrail_damage_cal.to_data import api_to_dict
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.image.image_tools import draw_text_by_line
from starrail_damage_cal.cal_damage import cal_info, cal_char_info

from ..utils.error_reply import CHAR_HINT
from ..utils.fonts.first_world import fw_font_28
from ..utils.excel.read_excel import light_cone_ranks
from ..utils.map.name_covert import name_to_avatar_id, alias_to_char_name
from ..utils.map.SR_MAP_PATH import (
    RelicId2Rarity,
    AvatarRelicScore,
    avatarId2Name,
)
from ..utils.resource.RESOURCE_PATH import (
    RELIC_PATH,
    SKILL_PATH,
    PLAYER_PATH,
    WEAPON_PATH,
    CHAR_PORTRAIT_PATH,
)
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
    "": ("天赋", "talent"),
    "MazeNormal": "dev_连携",
    "Maze": ("秘技", "technique"),
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


async def draw_char_img(char_data: Dict, sr_uid: str, msg: str) -> Union[bytes, str]:
    if isinstance(char_data, str):
        return char_data
    char = await cal_char_info(char_data)
    damage_len = 0
    damage_list = []
    if str(char.char_id) in skill_dict:
        damage_data = copy.deepcopy(char_data)
        damage_list = await cal_info(damage_data)
        damage_len = len(damage_list)
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
        Image.open(CHAR_PORTRAIT_PATH / f"{char.char_id}.png")
        .resize((1050, 1050))
        .convert("RGBA")
    )
    char_info.paste(char_img, (-220, -130), char_img)

    # 放属性图标
    attr_img = Image.open(TEXT_PATH / f"IconAttribute{char.char_element}.png")
    char_info.paste(attr_img, (540, 122), attr_img)

    # 放角色名
    char_img_draw = ImageDraw.Draw(char_info)
    char_img_draw.text((620, 162), char.char_name, (255, 255, 255), sr_font_38, "lm")
    if hasattr(sr_font_38, "getsize"):
        char_name_len = sr_font_38.getsize(char.char_name)[0]  # type: ignore
    else:
        bbox = sr_font_38.getbbox(char.char_name)
        char_name_len = bbox[2] - bbox[0]

    # 放等级
    char_img_draw.text(
        (620 + char_name_len + 50, 168),
        f"LV.{char.char_level!s}",
        white_color,
        sr_font_24,
        "mm",
    )

    # 放星级
    rarity_img = Image.open(
        TEXT_PATH / f"LightCore_Rarity{char.char_rarity}.png"
    ).resize((306, 72))
    char_info.paste(rarity_img, (490, 189), rarity_img)

    # 放命座
    rank_img = Image.open(TEXT_PATH / "ImgNewBg.png")
    rank_img_draw = ImageDraw.Draw(rank_img)
    rank_img_draw.text(
        (70, 44), f"{NUM_MAP[char.char_rank]}命", white_color, sr_font_28, "mm"
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
    # 生命值
    hp = int(char.base_attributes.get("hp"))
    add_hp = int(
        char.add_attr.get("HPDelta", 0)
        + hp
        * char.add_attr.get(
            "HPAddedRatio",
            0,
        )
    )
    attr_bg_draw.text((413, 31), f"{hp + add_hp}", white_color, sr_font_26, "rm")
    attr_bg_draw.text(
        (428, 31),
        f"(+{round(add_hp)!s})",
        (95, 251, 80),
        sr_font_26,
        anchor="lm",
    )
    # 攻击力
    attack = int(char.base_attributes["attack"])
    add_attack = int(
        char.add_attr.get("AttackDelta", 0)
        + attack * char.add_attr.get("AttackAddedRatio", 0)
    )
    attr_bg_draw.text(
        (413, 31 + 48),
        f"{attack + add_attack}",
        white_color,
        sr_font_26,
        "rm",
    )
    attr_bg_draw.text(
        (428, 31 + 48),
        f"(+{round(add_attack)!s})",
        (95, 251, 80),
        sr_font_26,
        anchor="lm",
    )
    # 防御力
    defence = int(char.base_attributes["defence"])
    add_defence = int(
        char.add_attr.get("DefenceDelta", 0)
        + defence * char.add_attr.get("DefenceAddedRatio", 0)
    )
    attr_bg_draw.text(
        (413, 31 + 48 * 2),
        f"{defence + add_defence}",
        white_color,
        sr_font_26,
        "rm",
    )
    attr_bg_draw.text(
        (428, 31 + 48 * 2),
        f"(+{round(add_defence)!s})",
        (95, 251, 80),
        sr_font_26,
        anchor="lm",
    )
    # 速度
    speed = int(char.base_attributes["speed"])
    add_speed = int(
        char.add_attr.get("SpeedDelta", 0)
        + speed * char.add_attr.get("SpeedAddedRatio", 0)
    )
    attr_bg_draw.text(
        (413, 31 + 48 * 3),
        f"{speed + add_speed}",
        white_color,
        sr_font_26,
        "rm",
    )
    attr_bg_draw.text(
        (428, 31 + 48 * 3),
        f"(+{round(add_speed)!s})",
        (95, 251, 80),
        sr_font_26,
        anchor="lm",
    )
    # 暴击率
    critical_chance = char.base_attributes["CriticalChanceBase"]
    critical_chance_base = char.add_attr.get("CriticalChanceBase", 0)
    critical_chance = (critical_chance + critical_chance_base) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 4),
        f"{critical_chance:.1f}%",
        white_color,
        sr_font_26,
        "rm",
    )
    # 暴击伤害
    critical_damage = char.base_attributes["CriticalDamageBase"]
    critical_damage_base = char.add_attr.get("CriticalDamageBase", 0)
    critical_damage = (critical_damage + critical_damage_base) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 5),
        f"{critical_damage:.1f}%",
        white_color,
        sr_font_26,
        "rm",
    )
    # 效果命中
    status_probability_base = char.add_attr.get("StatusProbabilityBase", 0) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 6),
        f"{status_probability_base:.1f}%",
        white_color,
        sr_font_26,
        "rm",
    )
    # 效果抵抗
    status_resistance_base = char.add_attr.get("StatusResistanceBase", 0) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 7),
        f"{status_resistance_base:.1f}%",
        white_color,
        sr_font_26,
        "rm",
    )
    # 击破特攻
    status_resistance_base = char.add_attr.get("BreakDamageAddedRatioBase", 0) * 100
    attr_bg_draw.text(
        (500, 31 + 48 * 8),
        f"{status_resistance_base:.1f}%",
        white_color,
        sr_font_26,
        "rm",
    )
    char_info.paste(attr_bg, (475, 256), attr_bg)

    # 命座
    for rank in range(6):
        rank_bg = Image.open(TEXT_PATH / "mz_bg.png")
        rank_no_bg = Image.open(TEXT_PATH / "mz_no_bg.png")
        if rank < char.char_rank:
            rank_img = (
                Image.open(SKILL_PATH / f"{char.char_id}{RANK_MAP[rank + 1]}")
                .convert("RGBA")
                .resize((50, 50))
            )
            rank_bg.paste(rank_img, (19, 19), rank_img)
            char_info.paste(rank_bg, (20 + rank * 80, 630), rank_bg)
        else:
            rank_img = (
                Image.open(SKILL_PATH / f"{char.char_id}{RANK_MAP[rank + 1]}")
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
    for skill in char.char_skill:
        skill_attr_img = Image.open(TEXT_PATH / f"skill_attr{i + 1}.png")
        skill_panel_img = Image.open(TEXT_PATH / "skill_panel.png")
        skill_img = (
            Image.open(
                SKILL_PATH / f'{char.char_id}_'
                f'{skill_type_map[skill["skillAttackType"]][1]}.png'
            )
            .convert("RGBA")
            .resize((55, 55))
        )
        skill_panel_img.paste(skill_img, (18, 15), skill_img)
        skill_panel_img.paste(skill_attr_img, (80, 10), skill_attr_img)
        skill_panel_img_draw = ImageDraw.Draw(skill_panel_img)
        skill_panel_img_draw.text(
            (108, 25),
            f'{skill_type_map[skill["skillAttackType"]][0]}',
            white_color,
            sr_font_26,
            "lm",
        )
        skill_panel_img_draw.text(
            (89, 55),
            f'Lv.{skill["skillLevel"]}',
            white_color,
            sr_font_26,
            "lm",
        )
        skill_panel_img_draw.text(
            (75, 90),
            f'{skill["skillName"]}',
            (105, 105, 105),
            sr_font_20,
            "mm",
        )
        skill_bg.paste(skill_panel_img, (50 + 187 * i, 35), skill_panel_img)
        i += 1
    char_info.paste(skill_bg, (0, 710), skill_bg)

    # 武器
    if char.equipment != {}:
        weapon_bg = Image.open(TEXT_PATH / "weapon_bg.png")
        weapon_id = char.equipment["equipmentID"]
        weapon_img = (
            Image.open(WEAPON_PATH / f"{weapon_id}.png")
            .convert("RGBA")
            .resize((170, 180))
        )
        weapon_bg.paste(weapon_img, (20, 90), weapon_img)
        weapon_bg_draw = ImageDraw.Draw(weapon_bg)
        weapon_bg_draw.text(
            (345, 47),
            f'{char.equipment["equipmentName"]}',
            white_color,
            sr_font_34,
            "lm",
        )
        if hasattr(sr_font_34, "getsize"):
            weapon_name_len = sr_font_34.getsize(  # type: ignore
                char.equipment["equipmentName"]
            )[0]
        else:
            bbox = sr_font_34.getbbox(char.equipment["equipmentName"])
            weapon_name_len = bbox[2] - bbox[0]
        # 放阶
        rank_img = Image.open(TEXT_PATH / "ImgNewBg.png")
        rank_img_draw = ImageDraw.Draw(rank_img)
        rank_img_draw.text(
            (70, 44),
            f'{NUM_MAP[char.equipment["equipmentRank"]]}阶',
            white_color,
            sr_font_28,
            "mm",
        )
        weapon_bg.paste(rank_img, (weapon_name_len + 330, 2), rank_img)

        rarity_img = Image.open(
            TEXT_PATH / f'LightCore_Rarity{char.equipment["equipmentRarity"]}.png'
        ).resize((306, 72))
        weapon_bg.paste(rarity_img, (223, 55), rarity_img)
        weapon_bg_draw.text(
            (498, 90),
            f'Lv.{char.equipment["equipmentLevel"]}',
            white_color,
            sr_font_28,
            "mm",
        )

        # 武器技能
        desc = light_cone_ranks[str(char.equipment["equipmentID"])]["desc"]
        desc_params = light_cone_ranks[str(char.equipment["equipmentID"])]["params"][
            char.equipment["equipmentRank"] - 1
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
                weapon_bg,
                (210, desctexty),  # type: ignore
                desctext,
                sr_font_24,
                "#F9F9F9",
                370,
            )
            desctexty += 28
        char_info.paste(weapon_bg, (0, 855), weapon_bg)
    else:
        char_img_draw.text(
            (525, 1005),
            "No light cone!",
            white_color,
            fw_font_28,
            "mm",
        )

    # 遗器
    if char.char_relic:
        weapon_rank_bg = Image.open(TEXT_PATH / "rank_bg.png")
        char_info.paste(weapon_rank_bg, (735, 880), weapon_rank_bg)
        relic_score = 0

        for relic in char.char_relic:
            rarity = RelicId2Rarity[str(relic["relicId"])]
            relic_img = Image.open(TEXT_PATH / f"yq_bg{rarity}.png")
            if str(relic["SetId"])[0] == "3":
                relic_piece_img = Image.open(
                    RELIC_PATH / f'{relic["SetId"]}_{relic["Type"] - 5}.png'
                )
            else:
                relic_piece_img = Image.open(
                    RELIC_PATH / f'{relic["SetId"]}_{relic["Type"] - 1}.png'
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
                f'{RelicId2Rarity[str(relic["relicId"])]}.png'
            ).resize((200, 48))
            relic_img.paste(rarity_img, (-10, 80), rarity_img)
            relic_img_draw = ImageDraw.Draw(relic_img)
            if len(relic["relicName"]) <= 5:
                main_name = relic["relicName"]
            else:
                main_name = relic["relicName"][:2] + relic["relicName"][4:]
            relic_img_draw.text(
                (30, 70),
                main_name,
                (255, 255, 255),
                sr_font_34,
                anchor="lm",
            )

            # 主属性
            main_value = relic["MainAffix"]["Value"]
            main_name: str = relic["MainAffix"]["Name"]
            main_level: int = relic["Level"]

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
                relic["MainAffix"]["Property"],
                main_value,
                char.char_name,
                True,
                relic["Type"],
            )
            single_relic_score += main_value_score
            for index, i in enumerate(relic["SubAffixList"]):
                subName: str = i["Name"]
                subCnt = i["Cnt"]
                subValue = i["Value"]
                subProperty = i["Property"]

                tmp_score = await get_relic_score(
                    subProperty, subValue, char.char_name, False, relic["Type"]
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

            char_info.paste(relic_img, RELIC_POS[str(relic["Type"])], relic_img)
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
            "No relic!",
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
        fw_font_28,
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
