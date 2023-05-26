import json
from typing import Dict
from pathlib import Path

from mpmath import mp

from ..Base.WeaponBase import BaseWeapon

path = Path(__file__).parent
with open(path / 'weapon_effect.json', 'r', encoding='utf-8') as f:
    weapon_effect = json.load(f)


mp.dps = 14


class IntheNight(BaseWeapon):
    def __init__(self, weapon: Dict):
        super().__init__(weapon)

    async def check(self):
        pass

    async def weapon_ability(self, char):
        char = await self.weapon_property_ability(char)
        char_speed = mp.mpf(char.base_attributes['speed'])
        count_ = min(6, int(mp.floor((char_speed - 100) / 10)))
        char.a_dmg += (
            mp.mpf(weapon_effect['23001']['Param']['a_dmg'][self.weapon_rank])
            * count_
        )
        char.e_dmg += (
            mp.mpf(weapon_effect['23001']['Param']['e_dmg'][self.weapon_rank])
            * count_
        )
        char.q_crit_dmg += (
            mp.mpf(
                weapon_effect['23001']['Param']['q_crit_dmg'][self.weapon_rank]
            )
            * count_
        )
        return char

    async def weapon_property_ability(self, char):
        char.CriticalChanceBase += mp.mpf(
            weapon_effect['23001']['AbilityProperty'][self.weapon_rank]
        )
        return char


class CruisingintheStellarSea(BaseWeapon):
    def __init__(self, weapon: Dict):
        super().__init__(weapon)

    async def check(self):
        # 装备者对生命值百分比小于等于50%的敌方目标
        # 装备者消灭敌方目标
        return True

    async def weapon_ability(self, char):
        char = await self.weapon_property_ability(char)
        if self.check():
            char.CriticalChanceBase += mp.mpf(
                weapon_effect['24001']['Param']['CriticalChance'][
                    self.weapon_rank
                ]
            )
            char.AttackAddedRatio += mp.mpf(
                weapon_effect['24001']['Param']['AttackAddedRatio'][
                    self.weapon_rank
                ]
            )
        return char

    async def weapon_property_ability(self, char):
        char.CriticalChanceBase += mp.mpf(
            weapon_effect['24001']['AbilityProperty'][self.weapon_rank]
        )
        return char


class HuntWeapon:
    def __new__(cls, weapon: Dict):
        if weapon['id'] == 24001:
            return CruisingintheStellarSea(weapon)
        if weapon['id'] == 23001:
            return IntheNight(weapon)

    async def check_ability(self):
        pass


class Weapon:
    def __new__(cls, weapon: Dict):
        if weapon['id'] == 24001 or weapon['id'] == 23001:
            return HuntWeapon(weapon)
