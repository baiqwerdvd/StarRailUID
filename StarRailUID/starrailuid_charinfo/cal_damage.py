import json
from pathlib import Path
from typing import Dict, List, Union

from .effect.Role import RoleInstance
from .mono.Character import Character
from .damage.Avatar import AvatarInstance

Excel_path = Path(__file__).parent / 'effect'
with Path.open(Excel_path / 'Excel' / 'SkillData.json', encoding='utf-8') as f:
    skill_dict = json.load(f)


async def cal_char_info(char_data: Dict):
    char: Character = Character(char_data)
    await char.get_equipment_info()
    await char.get_char_attribute_bonus()
    await char.get_relic_info()
    return char


async def cal(char_data: Dict):
    char = await cal_char_info(char_data)

    skill_info_list: List[List[Union[str, float]]] = []
    if str(char.char_id) in skill_dict:
        skill_list = skill_dict[str(char.char_id)]['skillList']
        skill_list = skill_list.keys()
        for skill_type in skill_list:
            role = RoleInstance(char)
            im_tmp = await role.cal_damage(skill_type)
            skill_info_list.append(im_tmp)
        return skill_info_list
    return '角色伤害计算未完成'

async def cal_info(char_data: Dict):
    char = await cal_char_info(char_data)
    avatar = AvatarInstance(char)
    skill_info_list = await avatar.gat_damage()
    return skill_info_list