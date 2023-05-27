import json
from pathlib import Path
from typing import Dict, List
from abc import abstractmethod

from mpmath import mp

from .Skill import BaseSkills
from ....utils.excel.read_excel import AvatarPromotion

path = Path(__file__).parent
with open(path / 'seele.json', 'r', encoding='utf-8') as f:
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

    def __init__(self, char: Dict, skills: List):
        self.Skill = BaseSkills(char=char, skills=skills)
        self.avatar_id = char['id']
        self.avatar_level = char['level']
        self.avatar_rank = char['rank']
        self.avatar_element = char['element']
        self.avatar_promotion = char['promotion']
        self.avatar_attribute_bonus = char['attribute_bonus']
        self.avatar_extra_ability = char['extra_ability']
        self.avatar_attribute = {}

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
        self.avatar_attribute['CriticalChance'] = mp.mpf(
            promotion["CriticalChance"]['Value']
        )
        # 暴击伤害
        self.avatar_attribute['CriticalDamage'] = mp.mpf(
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


class Seele(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(self, char: Dict, skills: List):
        super().__init__(char=char, skills=skills)
        self.Buff = BaseAvatarBuff(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 1:
            self.eidolon_attribute['CriticalDamageBase'] = mp.mpf(0.15)
        if self.avatar_rank >= 2:
            self.eidolon_attribute['SpeedAddedRatio'] = mp.mpf(0.5)

    def extra_ability(self):
        # 额外能力 割裂 抗性穿透提高20
        if 1102102 in self.Buff.extra_ability_id:
            self.extra_ability_attribute[
                'QuantumResistancePenetration'
            ] = mp.mpf(0.2)


class Avatar:
    def __new__(cls, char: Dict, skills: List):
        if char['id'] == 1102:
            return Seele(char, skills)