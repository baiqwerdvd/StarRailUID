from typing import Dict
from abc import abstractmethod

from mpmath import mp

from ....utils.excel.read_excel import AvatarPromotion

mp.dps = 14


class BaseSkills:
    @abstractmethod
    async def Basic_ATK(self):
        ...

    @abstractmethod
    async def Skill(self):
        ...

    @abstractmethod
    async def Ultimate(self):
        ...

    @abstractmethod
    async def Talent(self):
        ...

    @abstractmethod
    async def Technique(self):
        ...


class BaseAvatar:
    def __init__(self, char: Dict):
        self.avatar_id = char['id']
        self.avatar_level = char['level']
        self.avatar_rank = char['rank']
        self.avatar_promotion = char['promotion']
        self.avatar_attribute = {}

    async def get_attribute(self):
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


class Seele(BaseAvatar, BaseSkills):
    def __init__(self, char: Dict):
        super().__init__(char)

    async def Basic_ATK(self):
        pass

    async def Skill(self):
        pass

    async def Ultimate(self):
        pass

    async def Talent(self):
        pass

    async def Technique(self):
        pass


class Avatar:
    def __new__(cls, char: Dict):
        if char['id'] == 1102:
            return Seele(char)
