import json
from typing import Dict
from pathlib import Path

from mpmath import mp

from ..Base.WeaponBase import BaseWeapon

path = Path(__file__).parent.parent
with open(path / 'Excel' / 'weapon_effect.json', 'r', encoding='utf-8') as f:
    weapon_effect = json.load(f)


mp.dps = 14


class IntheNight(BaseWeapon):
    def __init__(self, weapon: Dict):
        super().__init__(weapon)

    async def check(self):
        pass

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        char_speed = mp.mpf(base_attr.get('speed', 0))
        count_ = min(6, int(mp.floor((char_speed - 100) / 10)))
        normal_dmg_add = attribute_bonus.get('NormalDmgAdd', 0)
        attribute_bonus['NormalDmgAdd'] = normal_dmg_add + (
            mp.mpf(
                weapon_effect['23001']['Param']['a_dmg'][self.weapon_rank - 1]
            )
            * count_
        )
        bp_skill_dmg_add = attribute_bonus.get('BPSkillDmgAdd', 0)
        attribute_bonus['BPSkillDmgAdd'] = bp_skill_dmg_add + (
            mp.mpf(
                weapon_effect['23001']['Param']['e_dmg'][self.weapon_rank - 1]
            )
            * count_
        )
        ultra_critical_chance_base = attribute_bonus.get(
            'Ultra_CriticalChanceBase', 0
        )
        attribute_bonus[
            'Ultra_CriticalChanceBase'
        ] = ultra_critical_chance_base + (
            mp.mpf(
                weapon_effect['23001']['Param']['q_crit_dmg'][
                    self.weapon_rank - 1
                ]
            )
            * count_
        )
        return attribute_bonus


class CruisingintheStellarSea(BaseWeapon):
    def __init__(self, weapon: Dict):
        super().__init__(weapon)

    async def check(self):
        # 装备者对生命值百分比小于等于50%的敌方目标
        # 装备者消灭敌方目标
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus[
                'CriticalChanceBase'
            ] = critical_chance_base + mp.mpf(
                weapon_effect['24001']['Param']['CriticalChance'][
                    self.weapon_rank - 1
                ]
            )
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
                weapon_effect['24001']['Param']['AttackAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


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
