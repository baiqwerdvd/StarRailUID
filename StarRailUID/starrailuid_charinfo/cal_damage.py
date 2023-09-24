from typing import Dict, List, Union

from .effect.Role import RoleInstance
from .mono.Character import Character


async def cal_char_info(char_data: Dict):
    char: Character = Character(char_data)
    await char.get_equipment_info()
    await char.get_char_attribute_bonus()
    await char.get_relic_info()
    return char


async def cal(char_data: Dict):
    char = await cal_char_info(char_data)

    skill_info_list: List[List[Union[str, float]]] = []
    if char.char_id in [
        1102,
        1204,
        1107,
        1213,
        1006,
        1005,
        1205,
        1208,
        1104,
        1209,
        1004,
        1003,
        1201,
        1212,
        1112,
    ]:
        if char.char_id == 1213:
            for skill_type in [
                'Normal',
                'Normal1',
                'Normal2',
                'Normal3',
                'Ultra',
            ]:
                role = RoleInstance(char)
                im_tmp = await role.cal_damage(skill_type)
                skill_info_list.append(im_tmp)
        elif char.char_id == 1005:
            for skill_type in ['Normal', 'BPSkill', 'Ultra', 'DOT']:
                role = RoleInstance(char)
                im_tmp = await role.cal_damage(skill_type)
                skill_info_list.append(im_tmp)
        elif char.char_id == 1112:
            for skill_type in ['Normal', 'BPSkill', 'Talent1']:
                role = RoleInstance(char)
                im_tmp = await role.cal_damage(skill_type)
                skill_info_list.append(im_tmp)
        elif char.char_id == 1212:
            for skill_type in ['Normal', 'BPSkill', 'BPSkill1', 'Ultra']:
                role = RoleInstance(char)
                im_tmp = await role.cal_damage(skill_type)
                skill_info_list.append(im_tmp)
        elif char.char_id == 1208:
            for skill_type in ['Normal', 'Ultra']:
                role = RoleInstance(char)
                im_tmp = await role.cal_damage(skill_type)
                skill_info_list.append(im_tmp)
        elif char.char_id in [1205, 1201]:
            for skill_type in ['Normal', 'Normal1', 'Ultra']:
                role = RoleInstance(char)
                im_tmp = await role.cal_damage(skill_type)
                skill_info_list.append(im_tmp)
        else:
            for skill_type in ['Normal', 'BPSkill', 'Ultra']:
                role = RoleInstance(char)
                im_tmp = await role.cal_damage(skill_type)
                skill_info_list.append(im_tmp)
        if char.char_id in [1204, 1107, 1005, 1205, 1209, 1003]:
            role = RoleInstance(char)
            im_tmp = await role.cal_damage('Talent')
            skill_info_list.append(im_tmp)
        return skill_info_list
    return '角色伤害计算未完成'
