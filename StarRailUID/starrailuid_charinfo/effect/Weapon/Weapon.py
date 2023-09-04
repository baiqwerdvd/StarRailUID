import json
from pathlib import Path
from typing import Dict

from mpmath import mp

from ..Base.model import DamageInstanceWeapon
from ..Base.WeaponBase import BaseWeapon

path = Path(__file__).parent.parent
with Path.open(path / 'Excel' / 'weapon_effect.json', encoding='utf-8') as f:
    weapon_effect = json.load(f)


mp.dps = 14


class Arrows(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者消灭敌方目标
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChance', 0)
            attribute_bonus['CriticalChance'] = critical_chance_base + mp.mpf(
                weapon_effect['20000']['Param']['CriticalChance'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


class ReturntoDarkness(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者消灭敌方目标
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            pass
        return attribute_bonus


class Swordplay(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者消灭敌方目标
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['21010']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


class DartingArrow(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者消灭敌方目标
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
                weapon_effect['20007']['Param']['AttackAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


class Adversarial(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者消灭敌方目标
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            speed_added_ratio = attribute_bonus.get('SpeedAddedRatio', 0)
            attribute_bonus['SpeedAddedRatio'] = speed_added_ratio + mp.mpf(
                weapon_effect['20014']['Param']['SpeedAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return None


class SubscribeforMore(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者的当前能量值等于其能量上限
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            normal_dmg_add = attribute_bonus.get('NormalDmgAdd', 0)
            attribute_bonus['NormalDmgAdd'] = normal_dmg_add + (
                mp.mpf(
                    weapon_effect['21017']['Param']['a_dmg'][
                        self.weapon_rank - 1
                    ]
                )
                * 2
            )
            bp_skill_dmg_add = attribute_bonus.get('BPSkillDmgAdd', 0)
            attribute_bonus['BPSkillDmgAdd'] = bp_skill_dmg_add + (
                mp.mpf(
                    weapon_effect['21017']['Param']['e_dmg'][
                        self.weapon_rank - 1
                    ]
                )
                * 2
            )
            return attribute_bonus
        return None


class RiverFlowsinSpring(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 进入战斗后,使装备者速度提高8%,造成的伤害提高12%。
        # 当装备者受到伤害后该效果失效,下个回合结束时该效果恢复。
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            speed_added_ratio = attribute_bonus.get('SpeedAddedRatio', 0)
            attribute_bonus['SpeedAddedRatio'] = speed_added_ratio + mp.mpf(
                weapon_effect['21024']['Param']['SpeedAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['21024']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return None


class SleepLiketheDead(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者的普攻或战技伤害未造成暴击时,使自身暴击率提高36%,持续1回合。
        # 该效果每3回合可以触发1次。
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            return attribute_bonus
        return None


class OnlySilenceRemains(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当场上的敌方目标数量小于等于2时
        return True

    async def weapon_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus[
                'CriticalChanceBase'
            ] = critical_chance_base + mp.mpf(
                weapon_effect['21003']['Param']['CriticalChance'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return None


class IntheNight(BaseWeapon):
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
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
    weapon_base_attributes: Dict
    def __init__(self, weapon: DamageInstanceWeapon):
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


# class HuntWeapon(
#     IntheNight, OnlySilenceRemains, SleepLiketheDead,
#     SubscribeforMore, Swordplay, DartingArrow, Adversarial,
#     RiverFlowsinSpring, Arrows, ReturntoDarkness
# ):
#     @classmethod
#     def create(cls, weapon: DamageInstanceWeapon):
#         if weapon.id_ == 24001:
#             return SleepLiketheDead(weapon)
#         if weapon.id_ == 23001:
#             return IntheNight(weapon)
#         if weapon.id_ == 21003:
#             return OnlySilenceRemains(weapon)
#         if weapon.id_ == 21024:
#             return RiverFlowsinSpring(weapon)
#         if weapon.id_ == 20014:
#             return Adversarial(weapon)
#         if weapon.id_ == 20007:
#             return DartingArrow(weapon)
#         if weapon.id_ == 21010:
#             return Swordplay(weapon)
#         if weapon.id_ == 21031:
#             return ReturntoDarkness(weapon)
#         if weapon.id_ == 20000:
#             return Arrows(weapon)
#         raise ValueError(f'未知武器id: {weapon.id_}')

#     async def check_ability(self):
#         pass


class Weapon(
    IntheNight, OnlySilenceRemains, SleepLiketheDead,
    SubscribeforMore, Swordplay, DartingArrow, Adversarial,
    RiverFlowsinSpring, Arrows, ReturntoDarkness
):
    @classmethod
    def create(cls, weapon: DamageInstanceWeapon):
        if weapon.id_ in [
            23001,
            21003,
            23012,
            24001,
            21024,
            21017,
            20014,
            20007,
            21010,
            21031,
            20000,
        ]:
            if weapon.id_ == 24001:
                return SleepLiketheDead(weapon)
            if weapon.id_ == 23001:
                return IntheNight(weapon)
            if weapon.id_ == 21003:
                return OnlySilenceRemains(weapon)
            if weapon.id_ == 21024:
                return RiverFlowsinSpring(weapon)
            if weapon.id_ == 20014:
                return Adversarial(weapon)
            if weapon.id_ == 20007:
                return DartingArrow(weapon)
            if weapon.id_ == 21010:
                return Swordplay(weapon)
            if weapon.id_ == 21031:
                return ReturntoDarkness(weapon)
            if weapon.id_ == 20000:
                return Arrows(weapon)
            raise ValueError(f'未知武器id: {weapon.id_}')
        else:
            raise ValueError(f'不支持的武器种类: {weapon.id_}')
