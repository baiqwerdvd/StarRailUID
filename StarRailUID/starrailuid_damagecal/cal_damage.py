from typing import Dict

from mpmath import mp

from .effect.Base.Role import RoleInstance
from ..starrailuid_charinfo.mono.Character import Character
from ..starrailuid_charinfo.draw_char_img import cal_char_info

mp.dps = 14


async def cal(char_data: Dict):
    char: Character = await cal_char_info(char_data)

    raw_data = {"avatar": {}, "weapon": {}, "relic": []}
    raw_data['avatar']['id'] = char.char_id
    raw_data['avatar']['level'] = char.char_level
    raw_data['avatar']['rank'] = char.char_rank
    raw_data['avatar']['element'] = char.char_element
    raw_data['avatar']['promotion'] = char.char_promotion
    raw_data['avatar']['attribute_bonus'] = char.attribute_bonus
    raw_data['avatar']['extra_ability'] = char.extra_ability

    raw_data['weapon']['id'] = char.equipment['equipmentID']
    raw_data['weapon']['level'] = char.equipment['equipmentLevel']
    raw_data['weapon']['rank'] = char.equipment['equipmentRank']
    raw_data['weapon']['promotion'] = char.equipment['equipmentPromotion']

    raw_data['relic'] = char.char_relic

    raw_data['skill'] = char.char_skill

    for skill_type in ['Normal', 'BPSkill', 'Ultra']:
        role = RoleInstance(raw_data)
        print(role)
        await role.cal_damage(skill_type)
    return '还没写完呢'
