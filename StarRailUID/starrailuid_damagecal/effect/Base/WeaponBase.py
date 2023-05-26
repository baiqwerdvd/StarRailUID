from typing import Dict
from abc import abstractmethod

from mpmath import mp

from ....utils.excel.read_excel import EquipmentPromotion

mp.dps = 14


class BaseWeapon:
    def __init__(self, weapon: Dict):
        self.weapon_id = weapon['id']
        self.weapon_level = weapon['level']
        self.weapon_rank = weapon['rank']
        self.weapon_promotion = weapon['promotion']
        self.weapon_attribute = {}

    @abstractmethod
    async def weapon_ability(self, char):
        '''
        战斗加成属性, 与 weapon_property_ability() 互斥
        '''
        ...

    @abstractmethod
    async def weapon_property_ability(self, char):
        '''
        面板加成属性, 与 weapon_ability() 互斥
        '''
        ...

    @abstractmethod
    async def check(self):
        ...

    async def get_attribute(self):
        promotion = EquipmentPromotion[str(self.weapon_id)][
            str(self.weapon_promotion)
        ]

        self.weapon_attribute['hp'] = mp.mpf(
            promotion["BaseHP"]['Value']
        ) + mp.mpf(promotion["BaseHPAdd"]['Value']) * (self.weapon_level - 1)

        self.weapon_attribute['attack'] = mp.mpf(
            promotion["BaseAttack"]['Value']
        ) + mp.mpf(promotion["BaseAttackAdd"]['Value']) * (
            self.weapon_level - 1
        )

        self.weapon_attribute['defence'] = mp.mpf(
            promotion["BaseDefence"]['Value']
        ) + mp.mpf(promotion["BaseDefenceAdd"]['Value']) * (
            self.weapon_level - 1
        )
