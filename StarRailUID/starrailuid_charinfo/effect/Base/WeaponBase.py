from typing import Dict
from abc import abstractmethod

from mpmath import mp

from .model import DamageInstanceWeapon
from ....utils.excel.read_excel import EquipmentPromotion
from ....utils.map.SR_MAP_PATH import EquipmentID2AbilityProperty

mp.dps = 14


class BaseWeapon:
    def __init__(self, weapon: DamageInstanceWeapon):
        self.weapon_id = weapon.id_
        self.weapon_level = weapon.level
        self.weapon_rank = weapon.rank
        self.weapon_promotion = weapon.promotion
        self.weapon_base_attribute = {}
        self.weapon_attribute = {}
        self.get_attribute()
        self.weapon_property_ability()

    @abstractmethod
    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        战斗加成属性, 与 weapon_property_ability() 互斥
        '''
        ...

    def weapon_property_ability(self):
        '''
        面板加成属性, 与 weapon_ability() 互斥
        '''
        ability_property = EquipmentID2AbilityProperty[str(self.weapon_id)]
        equip_ability_property = ability_property[str(self.weapon_rank)]
        for equip_ability in equip_ability_property:
            property_type = equip_ability['PropertyType']
            value = equip_ability['Value']['Value']
            if property_type in self.weapon_attribute:
                self.weapon_attribute[property_type] += value
            else:
                self.weapon_attribute[property_type] = value

    @abstractmethod
    async def check(self):
        ...

    def get_attribute(self):
        promotion = EquipmentPromotion[str(self.weapon_id)][
            str(self.weapon_promotion)
        ]

        self.weapon_base_attribute['hp'] = mp.mpf(
            promotion["BaseHP"]['Value']
        ) + mp.mpf(promotion["BaseHPAdd"]['Value']) * (self.weapon_level - 1)

        self.weapon_base_attribute['attack'] = mp.mpf(
            promotion["BaseAttack"]['Value']
        ) + mp.mpf(promotion["BaseAttackAdd"]['Value']) * (
            self.weapon_level - 1
        )

        self.weapon_base_attribute['defence'] = mp.mpf(
            promotion["BaseDefence"]['Value']
        ) + mp.mpf(promotion["BaseDefenceAdd"]['Value']) * (
            self.weapon_level - 1
        )
