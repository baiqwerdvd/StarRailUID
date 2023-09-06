import json
from typing import Dict
from pathlib import Path

from mpmath import mp

from ..Base.WeaponBase import BaseWeapon
from ..Base.model import DamageInstanceWeapon

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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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


# 拂晓之前
class BeforeDawn(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        bp_skill_dmg_add = attribute_bonus.get('BPSkillDmgAdd', 0)
        attribute_bonus['BPSkillDmgAdd'] = bp_skill_dmg_add + (
            mp.mpf(
                weapon_effect['23010']['Param']['e_dmg'][self.weapon_rank - 1]
            )
        )
        ultra_dmg_add = attribute_bonus.get('UltraDmgAdd', 0)
        attribute_bonus['UltraDmgAdd'] = ultra_dmg_add + (
            mp.mpf(
                weapon_effect['23010']['Param']['r_dmg'][self.weapon_rank - 1]
            )
        )
        talent_dmg_add = attribute_bonus.get('TalentDmgAdd', 0)
        attribute_bonus['TalentDmgAdd'] = talent_dmg_add + (
            mp.mpf(
                weapon_effect['23010']['Param']['t_dmg'][self.weapon_rank - 1]
            )
        )
        return attribute_bonus


class IntheNight(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        char_speed = (
            mp.mpf(base_attr.get('speed', 0))
            + mp.mpf(attribute_bonus.get('SpeedDelta', 0))
        ) * (mp.mpf(attribute_bonus.get('SpeedAddedRatio', 0)) + 1)
        print(char_speed)
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

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
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


class SeriousnessofBreakfast(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者造成伤害提高12%
        # 每消灭1个敌方目标，装备者的攻击力提高4%，该效果最多叠加3层。
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        all_damage_added_ratio = attribute_bonus.get('AllDamageAddedRatio', 0)
        attribute_bonus[
            'AllDamageAddedRatio'
        ] = all_damage_added_ratio + mp.mpf(
            weapon_effect['21027']['Param']['AllDamageAddedRatio'][
                self.weapon_rank - 1
            ]
        )
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + mp.mpf(
                    weapon_effect['21027']['Param']['AttackAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 3
            )
        return attribute_bonus


# 银河铁道之夜
class NightontheMilkyWay(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 场上每有1个敌方目标，使装备者的攻击力提高9%
        # 敌方目标的弱点被击破时，装备者造成的伤害提高30%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
                weapon_effect['23000']['Param']['AttackAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['23000']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return None


# 今日亦是和平的一日
class TodayIsAnotherPeacefulDay(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 根据装备者的能量上限，提高装备者造成的伤害：每点能量提高0.2%，最多计入160点
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        all_damage_added_ratio = attribute_bonus.get('AllDamageAddedRatio', 0)
        attribute_bonus['AllDamageAddedRatio'] = (
            all_damage_added_ratio
            + mp.mpf(
                weapon_effect['21034']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            * Ultra_Use
        )
        return attribute_bonus


# 天才们的休憩
class GeniusesRepose(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者攻击力提高16%
        # 当装备者消灭敌方目标后，暴击伤害提高24%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        # attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
        # attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
        # weapon_effect['21020']['Param']['AttackAddedRatio'][
        # self.weapon_rank - 1
        # ]
        # )
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus['CriticalDamageBase'] = critical_chance_base + (
                mp.mpf(
                    weapon_effect['21020']['Param']['CriticalDamageBase'][
                        self.weapon_rank - 1
                    ]
                )
            )
        return attribute_bonus


# 别让世界静下来
class MaketheWorldClamor(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 终结技造成的伤害提高32%。
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        ultra_dmg_add = attribute_bonus.get('UltraDmgAdd', 0)
        attribute_bonus['UltraDmgAdd'] = ultra_dmg_add + (
            mp.mpf(
                weapon_effect['21013']['Param']['r_dmg'][self.weapon_rank - 1]
            )
        )
        return attribute_bonus


# 「我」的诞生
class TheBirthoftheSelf(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 追加攻击造成的伤害提高30%
        # 若该敌方目标当前生命值百分比小于等于50%，则追加攻击造成的伤害额外提高30%。
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            talent_dmg_add = attribute_bonus.get('TalentDmgAdd', 0)
            attribute_bonus['TalentDmgAdd'] = talent_dmg_add + (
                mp.mpf(
                    weapon_effect['21006']['Param']['t_dmg'][
                        self.weapon_rank - 1
                    ]
                )
            )
            return attribute_bonus
        return None


# 秘密誓心
class ASecretVow(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 造成的伤害提高20%
        # 对当前生命值百分比大于等于装备者自身当前生命值百分比的敌方目标造成的伤害额外提高20%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['21012']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return None


# 比阳光更明亮的
class BrighterThantheSun(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者的暴击率提高18%
        # 当装备者施放普攻时，获得1层【龙吟】，持续2回合。每层【龙吟】使装备者的攻击力提高18%,【龙吟】最多叠加2层
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + mp.mpf(
                    weapon_effect['23015']['Param']['AttackAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 2
            )
        return attribute_bonus


# 到不了的彼岸
class TheUnreachableSide(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者的暴击率提高30%，生命上限提高30%
        # 当装备者受到攻击或装备者消耗自身生命值后，造成的伤害提高40%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        # critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
        # attribute_bonus[
        # 'CriticalChanceBase'
        # ] = critical_chance_base + mp.mpf(
        # weapon_effect['23009']['Param']['CriticalChance'][
        # self.weapon_rank - 1
        # ]
        # )
        # hp_added_ratio = attribute_bonus.get('HPAddedRatio', 0)
        # attribute_bonus[
        # 'HPAddedRatio'
        # ] = hp_added_ratio + mp.mpf(
        # weapon_effect['23009']['Param']['HPAddedRatio'][
        # self.weapon_rank - 1
        # ]
        # )
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['23009']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 无可取代的东西
class SomethingIrreplaceable(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者的攻击力提高24%
        # 当装备者消灭敌方目标或受到攻击后，造成的伤害提高24%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        # attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
        # attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
        # weapon_effect['23002']['Param']['AttackAddedRatio'][
        # self.weapon_rank - 1
        # ]
        # )
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['23002']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 记一位星神的陨落
class OntheFallofanAeon(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放攻击时，使装备者本场战斗中的攻击力提高8%，该效果最多叠加4层
        # 当装备者击破敌方目标弱点后，造成的伤害提高12%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + mp.mpf(
                    weapon_effect['24000']['Param']['AttackAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 4
            )
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['24000']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 无处可逃
class NowheretoRun(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者的攻击力提高24%
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        # attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
        # attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
        # weapon_effect['21033']['Param']['AttackAddedRatio'][
        # self.weapon_rank - 1
        # ]
        # )
        return attribute_bonus


# 汪！散步时间！
class WoofWalkTime(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者的攻击力提高10%
        # 对处于灼烧或裂伤状态的敌方目标造成的伤害提高16%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        # attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
        # attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
        # weapon_effect['21026']['Param']['AttackAddedRatio'][
        # self.weapon_rank - 1
        # ]
        # )
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['21026']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 在蓝天下
class UndertheBlueSky(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者攻击力提高16%
        # 当装备者消灭敌方目标后，暴击率提高12%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        # attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
        # attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
        # weapon_effect['21019']['Param']['AttackAddedRatio'][
        # self.weapon_rank - 1
        # ]
        # )
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus[
                'CriticalChanceBase'
            ] = critical_chance_base + mp.mpf(
                weapon_effect['21019']['Param']['CriticalChance'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 鼹鼠党欢迎你
class TheMolesWelcomeYou(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者施放普攻、战技或终结技攻击敌方目标后，分别获取一层【淘气值】。每层使装备者的攻击力提高12%。
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + mp.mpf(
                    weapon_effect['21005']['Param']['AttackAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 3
            )
        return attribute_bonus


# 雨一直下
class IncessantRain(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者对同时处于大于等于3个负面效果的敌方目标造成伤害时，暴击率提高12%
        # 持有【以太编码】的目标受到的伤害提高12%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            damage_ratio = attribute_bonus.get('DmgRatio', 0)
            attribute_bonus['DmgRatio'] = damage_ratio + mp.mpf(
                weapon_effect['23007']['Param']['DmgRatio'][
                    self.weapon_rank - 1
                ]
            )
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus[
                'CriticalChanceBase'
            ] = critical_chance_base + mp.mpf(
                weapon_effect['23007']['Param']['CriticalChance'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 只需等待
class PatienceIsAllYouNeed(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者造成的伤害提高24%
        # 装备者每次施放攻击后，速度提高4.8%，最多叠加3层。
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['23006']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )

            speed_added_ratio = attribute_bonus.get('SpeedAddedRatio', 0)
            attribute_bonus['SpeedAddedRatio'] = (
                speed_added_ratio
                + mp.mpf(
                    weapon_effect['23006']['Param']['SpeedAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 3
            )
        return attribute_bonus


# 以世界之名
class IntheNameoftheWorld(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者对陷入负面效果的敌方目标造成的伤害提高24%
        # 当装备者施放战技时，装备者此次攻击的效果命中提高18%
        # 当装备者施放战技时，装备者此次攻击的攻击力提高24%。
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['23004']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )

            a2_status_probability = attribute_bonus.get(
                'BPSkillStatusProbabilityBase', 0
            )
            attribute_bonus[
                'BPSkillStatusProbabilityBase'
            ] = a2_status_probability + mp.mpf(
                weapon_effect['23004']['Param']['A2_StatusProbability'][
                    self.weapon_rank - 1
                ]
            )

            a2_attack_added_ratio = attribute_bonus.get(
                'BPSkillAttackAddedRatio', 0
            )
            attribute_bonus[
                'BPSkillAttackAddedRatio'
            ] = a2_attack_added_ratio + mp.mpf(
                weapon_effect['23004']['Param']['A2_AttackAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 孤独的疗愈
class SolitaryHealing(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者的击破特攻提高20%
        # 装备者施放终结技时，使装备者造成的持续伤害提高24%
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        return attribute_bonus


# 新手任务开始前
class BeforetheTutorialMissionStarts(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者攻击防御力被降低的敌方目标后，恢复4点能量。
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        return attribute_bonus


# 后会有期
class WeWillMeetAgain(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者施放普攻或战技后，对随机1个受到攻击的敌方目标造成等同于自身48%攻击力的附加伤害。
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        return attribute_bonus


# 延长记号
class Fermata(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 对处于触电或风化状态的敌方目标造成的伤害提高16%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus[
                'AllDamageAddedRatio'
            ] = all_damage_added_ratio + mp.mpf(
                weapon_effect['21022']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 决心如汗珠般闪耀
class ResolutionShinesAsPearlsofSweat(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 对处于触电或风化状态的敌方目标造成的伤害提高16%
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            ignore_defence = attribute_bonus.get('ignore_defence', 0)
            attribute_bonus['ignore_defence'] = ignore_defence + mp.mpf(
                weapon_effect['21015']['Param']['ignore_defence'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 猎物的视线
class EyesofthePrey(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 造成的持续伤害提高24%。
        pass

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        return attribute_bonus


# 晚安与睡颜
class GoodNightandSleepWell(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 敌方目标每承受1个负面效果，装备者对其造成的伤害提高12%，最多叠加3层
        return True

    async def weapon_ability(
        self, Ultra_Use: int, base_attr: Dict, attribute_bonus: Dict
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + mp.mpf(
                    weapon_effect['21001']['Param']['AllDamageAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 3
            )
        return attribute_bonus


class Weapon:
    @classmethod
    def create(cls, weapon: DamageInstanceWeapon):
        if weapon.id_ in [
            23007,
            21005,
            21019,
            21026,
            21033,
            24000,
            23002,
            23009,
            23015,
            21012,
            21006,
            21013,
            21027,
            21020,
            21034,
            23000,
            23010,
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
            23006,
            23004,
            24003,
            22000,
            21029,
            21022,
            21015,
            21008,
            21001,
        ]:
            if weapon.id_ == 21001:
                return GoodNightandSleepWell(weapon)
            if weapon.id_ == 21008:
                return EyesofthePrey(weapon)
            if weapon.id_ == 21015:
                return ResolutionShinesAsPearlsofSweat(weapon)
            if weapon.id_ == 21022:
                return Fermata(weapon)
            if weapon.id_ == 21029:
                return WeWillMeetAgain(weapon)
            if weapon.id_ == 22000:
                return BeforetheTutorialMissionStarts(weapon)
            if weapon.id_ == 24003:
                return SolitaryHealing(weapon)
            if weapon.id_ == 23004:
                return IntheNameoftheWorld(weapon)
            if weapon.id_ == 23006:
                return PatienceIsAllYouNeed(weapon)
            if weapon.id_ == 23007:
                return IncessantRain(weapon)
            if weapon.id_ == 21005:
                return TheMolesWelcomeYou(weapon)
            if weapon.id_ == 21019:
                return UndertheBlueSky(weapon)
            if weapon.id_ == 21026:
                return WoofWalkTime(weapon)
            if weapon.id_ == 21033:
                return NowheretoRun(weapon)
            if weapon.id_ == 24000:
                return OntheFallofanAeon(weapon)
            if weapon.id_ == 23002:
                return SomethingIrreplaceable(weapon)
            if weapon.id_ == 23009:
                return TheUnreachableSide(weapon)
            if weapon.id_ == 23015:
                return BrighterThantheSun(weapon)
            if weapon.id_ == 21012:
                return ASecretVow(weapon)
            if weapon.id_ == 21006:
                return TheBirthoftheSelf(weapon)
            if weapon.id_ == 21013:
                return MaketheWorldClamor(weapon)
            if weapon.id_ == 21020:
                return GeniusesRepose(weapon)
            if weapon.id_ == 21027:
                return SeriousnessofBreakfast(weapon)
            if weapon.id_ == 21034:
                return TodayIsAnotherPeacefulDay(weapon)
            if weapon.id_ == 23000:
                return NightontheMilkyWay(weapon)
            if weapon.id_ == 23010:
                return BeforeDawn(weapon)
            if weapon.id_ == 24001:
                return CruisingintheStellarSea(weapon)
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
