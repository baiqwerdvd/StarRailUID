from typing import Dict

from mpmath import mp

from .draw_char_img import cal_char_info
from .effect.Role import RoleInstance

mp.dps = 14


async def cal(char_data: Dict):
    char = await cal_char_info(char_data)

    im = []

    for skill_type in ['Normal', 'BPSkill', 'Ultra']:
        role = RoleInstance(char)
        im_tmp = await role.cal_damage(skill_type)
        im.append(im_tmp)
    return im
