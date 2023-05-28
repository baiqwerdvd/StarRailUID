import json
from pathlib import Path
from typing import Dict, List
from abc import abstractmethod

from mpmath import mp

from .SkillBase import BaseSkills
from ....utils.excel.read_excel import AvatarPromotion

path = Path(__file__).parent.parent
with open(path / 'Excel' / 'seele.json', 'r', encoding='utf-8') as f:
    skill_dict = json.load(f)

mp.dps = 14


class BaseAvatarBuff:
    def __init__(self, char: Dict, skills: List):
        self.extra_ability_id = []
        for extra_ability in char['extra_ability']:
            self.extra_ability_id.append(extra_ability['extraAbilityId'])

    @abstractmethod
    async def Technique(self):
        ...

    @abstractmethod
    async def eidolons(self):
        ...

    @abstractmethod
    async def extra_ability(self):
        ...


class BaseAvatar:
    Skill: BaseSkills
    Buff: BaseAvatarBuff

    def __init__(self, char: Dict, skills: List):
        self.Skill = BaseSkills(char=char, skills=skills)
        self.Buff = BaseAvatarBuff(char=char, skills=skills)
        self.avatar_id = char['id']
        self.avatar_level = char['level']
        self.avatar_rank = char['rank']
        self.avatar_element = char['element']
        self.avatar_promotion = char['promotion']
        self.avatar_attribute_bonus = char['attribute_bonus']
        self.avatar_extra_ability = char['extra_ability']
        self.avatar_attribute = {}
        self.get_attribute()

    def get_attribute(self):
        promotion = AvatarPromotion[str(self.avatar_id)][
            str(self.avatar_promotion)
        ]

        # 攻击力
        self.avatar_attribute['attack'] = mp.mpf(
            promotion["AttackBase"]['Value']
        ) + mp.mpf(promotion["AttackAdd"]['Value']) * (self.avatar_level - 1)
        # 防御力
        self.avatar_attribute['defence'] = mp.mpf(
            promotion["DefenceBase"]['Value']
        ) + mp.mpf(promotion["DefenceAdd"]['Value']) * (self.avatar_level - 1)
        # 血量
        self.avatar_attribute['hp'] = mp.mpf(
            promotion["HPBase"]['Value']
        ) + mp.mpf(promotion["HPAdd"]['Value']) * (self.avatar_level - 1)
        # 速度
        self.avatar_attribute['speed'] = mp.mpf(
            promotion["SpeedBase"]['Value']
        )
        # 暴击率
        self.avatar_attribute['CriticalChanceBase'] = mp.mpf(
            promotion["CriticalChance"]['Value']
        )
        # 暴击伤害
        self.avatar_attribute['CriticalDamageBase'] = mp.mpf(
            promotion["CriticalDamage"]['Value']
        )
        # 嘲讽
        self.avatar_attribute['BaseAggro'] = mp.mpf(
            promotion["BaseAggro"]['Value']
        )

    def Normal(self):
        return mp.mpf(
            skill_dict[str(self.avatar_id)]['Normal'][
                self.Skill.Normal_.level - 1
            ]
        )

    def BPSkill(self):
        return mp.mpf(
            skill_dict[str(self.avatar_id)]['BPSkill'][
                self.Skill.BPSkill_.level - 1
            ]
        )

    def Ultra(self):
        return mp.mpf(
            skill_dict[str(self.avatar_id)]['Ultra'][
                self.Skill.Ultra_.level - 1
            ]
        )

    def Maze(self):
        return mp.mpf(
            skill_dict[str(self.avatar_id)]['Maze'][self.Skill.Maze_.level - 1]
        )

    def Talent(self):
        return mp.mpf(
            skill_dict[str(self.avatar_id)][''][self.Skill.Talent_.level - 1]
        )
