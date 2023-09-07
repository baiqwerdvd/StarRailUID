import json
from typing import List
from pathlib import Path
from abc import abstractmethod

from mpmath import mp

from .SkillBase import BaseSkills
from ....utils.excel.read_excel import AvatarPromotion
from .model import DamageInstanceSkill, DamageInstanceAvatar

path = Path(__file__).parent.parent
with Path.open(path / 'Excel' / 'seele.json', encoding='utf-8') as f:
    skill_dict = json.load(f)

mp.dps = 14


class BaseAvatarBuff:
    @classmethod
    def create(
        cls, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        cls.extra_ability_id = []
        if char.extra_ability:
            for extra_ability in char.extra_ability:
                cls.extra_ability_id.append(extra_ability['extraAbilityId'])
        return cls

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
    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        self.Skill = BaseSkills.create(char=char, skills=skills)
        self.Buff = BaseAvatarBuff.create(char=char, skills=skills)
        self.avatar_id = char.id_
        self.avatar_level = char.level
        self.avatar_rank = char.rank
        self.avatar_element = char.element
        self.avatar_promotion = char.promotion
        self.avatar_attribute_bonus = char.attribute_bonus
        self.avatar_extra_ability = char.extra_ability
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

    def Skill_Info(self, skill_type):
        skill_info = skill_dict[str(self.avatar_id)]['skilllist'][skill_type]
        return skill_info

    def Normalnum(self, skill_type):
        return mp.mpf(
            skill_dict[str(self.avatar_id)][skill_type][
                self.Skill.Normal_.level - 1
            ]
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
            skill_dict[str(self.avatar_id)]['Talent'][
                self.Skill.Talent_.level - 1
            ]
        )

    def BPSkill_num(self, skill_type):
        return mp.mpf(
            skill_dict[str(self.avatar_id)][skill_type][
                self.Skill.BPSkill_.level - 1
            ]
        )

    def Ultra_num(self, skill_type):
        return mp.mpf(
            skill_dict[str(self.avatar_id)][skill_type][
                self.Skill.Ultra_.level - 1
            ]
        )

    def Talent_num(self, skill_type):
        return mp.mpf(
            skill_dict[str(self.avatar_id)][skill_type][
                self.Skill.Talent_.level - 1
            ]
        )

    def Talent_add(self):
        if self.avatar_id in [1102]:
            return mp.mpf(
                skill_dict[str(self.avatar_id)]['Talent'][
                    self.Skill.Talent_.level - 1
                ]
            )
        elif self.avatar_id in [1205]:
            return mp.mpf(
                skill_dict[str(self.avatar_id)]['BPSkill'][
                    self.Skill.BPSkill_.level - 1
                ]
            )
        else:
            return mp.mpf(0)

    def Ultra_Use(self):
        return skill_dict[str(self.avatar_id)]['Ultra_Use'][0]
