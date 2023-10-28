import json
from pathlib import Path
from typing import Dict

from ..Base.model import DamageInstanceWeapon
from ..Base.WeaponBase import BaseWeapon

path = Path(__file__).parent.parent
with Path.open(path / 'Excel' / 'weapon_effect.json', encoding='utf-8') as f:
    weapon_effect = json.load(f)


class Arrows(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者消灭敌方目标
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChance', 0)
            attribute_bonus['CriticalChance'] = (
                critical_chance_base
                + weapon_effect['20000']['Param']['CriticalChance'][
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            pass
        return attribute_bonus


class Swordplay(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者多次击中同一敌方目标时, 每次造成的伤害提高8%, 该效果最多叠加5层
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + (
                    weapon_effect['21010']['Param']['AllDamageAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 5
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + weapon_effect['20007']['Param']['AttackAddedRatio'][
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            speed_added_ratio = attribute_bonus.get('SpeedAddedRatio', 0)
            attribute_bonus['SpeedAddedRatio'] = (
                speed_added_ratio
                + weapon_effect['20014']['Param']['SpeedAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return attribute_bonus


class SubscribeforMore(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者的当前能量值等于其能量上限
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            normal_dmg_add = attribute_bonus.get('NormalDmgAdd', 0)
            attribute_bonus['NormalDmgAdd'] = (
                normal_dmg_add
                + (
                    weapon_effect['21017']['Param']['a_dmg'][
                        self.weapon_rank - 1
                    ]
                )
                * 2
            )
            bp_skill_dmg_add = attribute_bonus.get('BPSkillDmgAdd', 0)
            attribute_bonus['BPSkillDmgAdd'] = (
                bp_skill_dmg_add
                + (
                    weapon_effect['21017']['Param']['e_dmg'][
                        self.weapon_rank - 1
                    ]
                )
                * 2
            )
            return attribute_bonus
        return attribute_bonus


class RiverFlowsinSpring(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 进入战斗后,使装备者速度提高8%,造成的伤害提高12%。
        # 当装备者受到伤害后该效果失效,下个回合结束时该效果恢复。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            speed_added_ratio = attribute_bonus.get('SpeedAddedRatio', 0)
            attribute_bonus['SpeedAddedRatio'] = (
                speed_added_ratio
                + weapon_effect['21024']['Param']['SpeedAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['21024']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return attribute_bonus


class OnlySilenceRemains(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当场上的敌方目标数量小于等于2时
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus['CriticalChanceBase'] = (
                critical_chance_base
                + weapon_effect['21003']['Param']['CriticalChance'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return attribute_bonus


# 拂晓之前
class BeforeDawn(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        bp_skill_dmg_add = attribute_bonus.get('BPSkillDmgAdd', 0)
        attribute_bonus['BPSkillDmgAdd'] = (
            bp_skill_dmg_add
            + (weapon_effect['23010']['Param']['e_dmg'][self.weapon_rank - 1])
        )
        ultra_dmg_add = attribute_bonus.get('UltraDmgAdd', 0)
        attribute_bonus['UltraDmgAdd'] = (
            ultra_dmg_add
            + (weapon_effect['23010']['Param']['r_dmg'][self.weapon_rank - 1])
        )
        talent_dmg_add = attribute_bonus.get('TalentDmgAdd', 0)
        attribute_bonus['TalentDmgAdd'] = (
            talent_dmg_add
            + (weapon_effect['23010']['Param']['t_dmg'][self.weapon_rank - 1])
        )
        return attribute_bonus


class IntheNight(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        char_speed = (
            base_attr.get('speed', 0) + attribute_bonus.get('SpeedDelta', 0)
        ) * (attribute_bonus.get('SpeedAddedRatio', 0) + 1)
        count_ = min(6, int((char_speed - 100) / 10))
        normal_dmg_add = attribute_bonus.get('NormalDmgAdd', 0)
        attribute_bonus['NormalDmgAdd'] = (
            normal_dmg_add
            + (weapon_effect['23001']['Param']['a_dmg'][self.weapon_rank - 1])
            * count_
        )
        bp_skill_dmg_add = attribute_bonus.get('BPSkillDmgAdd', 0)
        attribute_bonus['BPSkillDmgAdd'] = (
            bp_skill_dmg_add
            + (weapon_effect['23001']['Param']['e_dmg'][self.weapon_rank - 1])
            * count_
        )
        ultra_critical_chance_base = attribute_bonus.get(
            'Ultra_CriticalDamageBase', 0
        )
        attribute_bonus['Ultra_CriticalDamageBase'] = (
            ultra_critical_chance_base
            + (
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus['CriticalChanceBase'] = (
                critical_chance_base
                + weapon_effect['24001']['Param']['CriticalChance'][
                    self.weapon_rank - 1
                ]
            )
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + weapon_effect['24001']['Param']['AttackAddedRatio'][
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
        # 每消灭1个敌方目标, 装备者的攻击力提高4%, 该效果最多叠加3层。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        all_damage_added_ratio = attribute_bonus.get('AllDamageAddedRatio', 0)
        attribute_bonus['AllDamageAddedRatio'] = (
            all_damage_added_ratio
            + weapon_effect['21027']['Param']['AllDamageAddedRatio'][
                self.weapon_rank - 1
            ]
        )
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + (
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
        # 场上每有1个敌方目标, 使装备者的攻击力提高9%
        # 敌方目标的弱点被击破时, 装备者造成的伤害提高30%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + weapon_effect['23000']['Param']['AttackAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['23000']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return attribute_bonus


# 今日亦是和平的一日
class TodayIsAnotherPeacefulDay(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 根据装备者的能量上限, 提高装备者造成的伤害: 每点能量提高0.2%, 最多计入160点
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        all_damage_added_ratio = attribute_bonus.get('AllDamageAddedRatio', 0)
        attribute_bonus['AllDamageAddedRatio'] = (
            all_damage_added_ratio
            + (
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
        # 当装备者消灭敌方目标后, 暴击伤害提高24%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus['CriticalDamageBase'] = (
                critical_chance_base
                + (
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        ultra_dmg_add = attribute_bonus.get('UltraDmgAdd', 0)
        attribute_bonus['UltraDmgAdd'] = (
            ultra_dmg_add
            + (weapon_effect['21013']['Param']['r_dmg'][self.weapon_rank - 1])
        )
        return attribute_bonus


# 「我」的诞生
class TheBirthoftheSelf(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 追加攻击造成的伤害提高30%
        # 若该敌方目标当前生命值百分比小于等于50%, 则追加攻击造成的伤害额外提高30%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            talent_dmg_add = attribute_bonus.get('TalentDmgAdd', 0)
            attribute_bonus['TalentDmgAdd'] = (
                talent_dmg_add
                + (
                    weapon_effect['21006']['Param']['t_dmg'][
                        self.weapon_rank - 1
                    ]
                )
            )
            return attribute_bonus
        return attribute_bonus


# 秘密誓心
class ASecretVow(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 造成的伤害提高20%
        # 对当前生命值百分比大于等于装备者自身当前生命值百分比的敌方目标
        # 造成的伤害额外提高20%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['21012']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            return attribute_bonus
        return attribute_bonus


# 比阳光更明亮的
class BrighterThantheSun(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者的暴击率提高18%
        # 当装备者施放普攻时, 获得1层【龙吟】, 持续2回合。
        # 每层【龙吟】使装备者的攻击力提高18%,【龙吟】最多叠加2层
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + (
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
        # 装备者的暴击率提高30%, 生命上限提高30%
        # 当装备者受到攻击或装备者消耗自身生命值后, 造成的伤害提高40%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['23009']['Param']['AllDamageAddedRatio'][
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
        # 当装备者消灭敌方目标或受到攻击后, 造成的伤害提高24%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['23002']['Param']['AllDamageAddedRatio'][
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
        # 当装备者施放攻击时, 使装备者本场战斗中的攻击力提高8%, 该效果最多叠加4层
        # 当装备者击破敌方目标弱点后, 造成的伤害提高12%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + (
                    weapon_effect['24000']['Param']['AttackAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 4
            )
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['24000']['Param']['AllDamageAddedRatio'][
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 汪! 散步时间!
class WoofWalkTime(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者的攻击力提高10%
        # 对处于灼烧或裂伤状态的敌方目标造成的伤害提高16%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
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
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['21026']['Param']['AllDamageAddedRatio'][
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
        # 当装备者消灭敌方目标后, 暴击率提高12%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        # attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
        # attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
        # weapon_effect['21019']['Param']['AttackAddedRatio'][
        # self.weapon_rank - 1
        # ]
        # )
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus['CriticalChanceBase'] = (
                critical_chance_base
                + weapon_effect['21019']['Param']['CriticalChance'][
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
        # 装备者施放普攻、战技或终结技攻击敌方目标后,
        # 分别获取一层【淘气值】。每层使装备者的攻击力提高12%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + (
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
        # 当装备者对同时处于大于等于3个负面效果的敌方目标造成伤害时, 暴击率提高12%
        # 持有【以太编码】的目标受到的伤害提高12%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            damage_ratio = attribute_bonus.get('DmgRatio', 0)
            attribute_bonus['DmgRatio'] = (
                damage_ratio
                + weapon_effect['23007']['Param']['DmgRatio'][
                    self.weapon_rank - 1
                ]
            )
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus['CriticalChanceBase'] = (
                critical_chance_base
                + weapon_effect['23007']['Param']['CriticalChance'][
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
        # 装备者每次施放攻击后, 速度提高4.8%, 最多叠加3层。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['23006']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )

            speed_added_ratio = attribute_bonus.get('SpeedAddedRatio', 0)
            attribute_bonus['SpeedAddedRatio'] = (
                speed_added_ratio
                + (
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
        # 当装备者施放战技时, 装备者此次攻击的效果命中提高18%
        # 当装备者施放战技时, 装备者此次攻击的攻击力提高24%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['23004']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )

            a2_status_probability = attribute_bonus.get(
                'BPSkillStatusProbabilityBase', 0
            )
            attribute_bonus['BPSkillStatusProbabilityBase'] = (
                a2_status_probability
                + weapon_effect['23004']['Param']['A2_StatusProbability'][
                    self.weapon_rank - 1
                ]
            )

            a2_attack_added_ratio = attribute_bonus.get(
                'BPSkillAttackAddedRatio', 0
            )
            attribute_bonus['BPSkillAttackAddedRatio'] = (
                a2_attack_added_ratio
                + weapon_effect['23004']['Param']['A2_AttackAddedRatio'][
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
        # 装备者施放终结技时, 使装备者造成的持续伤害提高24%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 新手任务开始前
class BeforetheTutorialMissionStarts(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者攻击防御力被降低的敌方目标后, 恢复4点能量。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 后会有期
class WeWillMeetAgain(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者施放普攻或战技后,
        # 对随机1个受到攻击的敌方目标造成等同于自身48%攻击力的附加伤害。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['21022']['Param']['AllDamageAddedRatio'][
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            ignore_defence = attribute_bonus.get('ignore_defence', 0)
            attribute_bonus['ignore_defence'] = (
                ignore_defence
                + weapon_effect['21015']['Param']['ignore_defence'][
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
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        dot_dmg_add = attribute_bonus.get('DOTDmgAdd', 0)
        attribute_bonus['DOTDmgAdd'] = (
            dot_dmg_add
            + weapon_effect['21008']['Param']['DOTDmgAdd'][
                self.weapon_rank - 1
            ]
        )
        return attribute_bonus


# 晚安与睡颜
class GoodNightandSleepWell(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 敌方目标每承受1个负面效果, 装备者对其造成的伤害提高12%, 最多叠加3层
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + (
                    weapon_effect['21001']['Param']['AllDamageAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 3
            )
        return attribute_bonus


# 她已闭上双眼
class SheAlreadyShutHerEyes(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者的生命值降低时, 使我方全体造成的伤害提高15%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + (
                    weapon_effect['23011']['Param']['AllDamageAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 3
            )
        return attribute_bonus


# 制胜的瞬间
class MomentofVictory(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者受到攻击后, 防御力额外提高24%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            defence_added_ratio = attribute_bonus.get('DefenceAddedRatio', 0)
            attribute_bonus['DefenceAddedRatio'] = (
                defence_added_ratio
                + weapon_effect['23005']['Param']['DefenceAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 记忆的质料
class TextureofMemories(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # ...
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 这就是我啦
class ThisIsMe(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者施放终结技时造成的伤害值提高, 提高数值等同于装备者防御力的60%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 我们是地火
class WeAreWildfire(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 战斗开始时, 使我方全体受到的伤害降低8%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 宇宙市场趋势
class TrendoftheUniversalMarket(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者受到攻击后, 有100%的基础概率使敌方目标陷入灼烧状态,
        # 每回合造成等同于装备者40%防御力的持续伤害
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 朗道的选择
class LandausChoice(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者受到攻击的概率提高, 同时受到的伤害降低16%。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 余生的第一天
class DayOneofMyNewLife(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 进入战斗后, 使我方全体的全属性抗性提高8%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 开疆
class Pioneering(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 进入战斗后, 使我方全体的全属性抗性提高8%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 戍御
class Defense(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 进入战斗后, 使我方全体的全属性抗性提高8%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 琥珀
class Amber(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者当前生命值百分比小于50%时, 其防御力额外提高16%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            defence_added_ratio = attribute_bonus.get('DefenceAddedRatio', 0)
            attribute_bonus['DefenceAddedRatio'] = (
                defence_added_ratio
                + weapon_effect['20003']['Param']['DefenceAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 俱殁
class MutualDemise(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者当前生命值百分比小于80%时, 暴击率提高12%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus['CriticalChanceBase'] = (
                critical_chance_base
                + weapon_effect['20016']['Param']['CriticalChance'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 乐圮
class ShatteredHome(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者对当前生命值百分比大于50%的敌方目标造成的伤害提高20%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['20009']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 天倾
class CollapsingSky(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者普攻和战技造成的伤害提高20%。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        normal_dmg_add = attribute_bonus.get('NormalDmgAdd', 0)
        attribute_bonus['NormalDmgAdd'] = (
            normal_dmg_add
            + (weapon_effect['20002']['Param']['a_dmg'][self.weapon_rank - 1])
        )
        bp_skill_dmg_add = attribute_bonus.get('BPSkillDmgAdd', 0)
        attribute_bonus['BPSkillDmgAdd'] = (
            bp_skill_dmg_add
            + (weapon_effect['20002']['Param']['e_dmg'][self.weapon_rank - 1])
        )
        return attribute_bonus


# 匿影
class HiddenShadow(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 施放战技后, 使装备者的下一次普攻对敌方目标造成等同于自身60%攻击力的附加伤害。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 渊环
class Loop(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者对减速状态下的敌方目标造成的伤害提高24%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            all_damage_added_ratio = attribute_bonus.get(
                'AllDamageAddedRatio', 0
            )
            attribute_bonus['AllDamageAddedRatio'] = (
                all_damage_added_ratio
                + weapon_effect['20009']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 幽邃
class Void(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 战斗开始时, 使装备者的效果命中提高20%, 持续3回合。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            status_probability = attribute_bonus.get(
                'StatusProbabilityBase', 0
            )
            attribute_bonus['StatusProbabilityBase'] = (
                status_probability
                + weapon_effect['20004']['Param']['StatusProbability'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 睿见
class Sagacity(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放终结技时, 攻击力提高24%, 持续2回合。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            a3_attack_added_ratio = attribute_bonus.get(
                'UltraAttackAddedRatio', 0
            )
            attribute_bonus['UltraAttackAddedRatio'] = (
                a3_attack_added_ratio
                + weapon_effect['20020']['Param']['A3_AttackAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        return attribute_bonus


# 灵钥
class Passkey(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者施放战技后额外恢复8点能量
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 智库
class DataBank(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者终结技造成的伤害提高28%。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        ultra_dmg_add = attribute_bonus.get('UltraDmgAdd', 0)
        attribute_bonus['UltraDmgAdd'] = (
            ultra_dmg_add
            + (weapon_effect['20006']['Param']['r_dmg'][self.weapon_rank - 1])
        )
        return attribute_bonus


# 此身为剑
class Thisbodyisasword(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当队友受到攻击或消耗生命值后, 装备者获得1层【月蚀】,
        # 最多叠加3层。每层【月蚀】使装备者下一次攻击造成的伤害提高14%。
        # 叠满3层时, 额外使该次攻击无视目标12%的防御力。该效果在装备者施放攻击后解除。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        all_damage_added_ratio = attribute_bonus.get('AllDamageAddedRatio', 0)
        attribute_bonus['AllDamageAddedRatio'] = (
            all_damage_added_ratio
            + (
                weapon_effect['23014']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
            * 3
        )

        resistance_penetration = attribute_bonus.get(
            'AllDamageResistancePenetration', 0
        )
        attribute_bonus['AllDamageResistancePenetration'] = (
            resistance_penetration
            + (
                weapon_effect['23014']['Param']['ResistancePenetration'][
                    self.weapon_rank - 1
                ]
            )
        )

        return attribute_bonus


# 如泥酣眠
class SleepLiketheDead(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者的普攻或战技伤害未造成暴击时,使自身暴击率提高36%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if not await self.check():
            return attribute_bonus
        critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
        attribute_bonus['CriticalChanceBase'] = (
            critical_chance_base
            + weapon_effect['23012']['Param']['CriticalChance'][
                self.weapon_rank - 1
            ]
        )
        return attribute_bonus


# 烦恼着,幸福着
class WorrisomeBlissf(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者施放追加攻击后,使目标陷入【温驯】状态,该效果最多叠加2层.我方目标击中【温驯】状态下的敌方目标时,每层【温驯】使造成的暴击伤害提高12%
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        critical_chance_base = attribute_bonus.get('TalentDmgAdd', 0)
        attribute_bonus['TalentDmgAdd'] = (
            critical_chance_base
            + weapon_effect['23016']['Param']['TalentDmgAdd'][
                self.weapon_rank - 1
            ]
        )
        if await self.check():
            critical_chance_base = attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus['CriticalDamageBase'] = (
                critical_chance_base
                + (
                    weapon_effect['23016']['Param']['CriticalDamageBase'][
                        self.weapon_rank - 1
                    ]
                )
                * 2
            )
        return attribute_bonus


# 片刻, 留在眼底
class AnInstanceBeforeAGaze(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放终结技时, 根据装备者的能量上限, 提高装备者终结技造成的伤害: 每点能量提高0.36%, 最多计入180点。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            critical_chance_base = attribute_bonus.get('UltraDmgAdd', 0)
            attribute_bonus['UltraDmgAdd'] = (
                critical_chance_base
                + (
                    weapon_effect['23018']['Param']['r_dmg'][
                        self.weapon_rank - 1
                    ]
                )
                * Ultra_Use
            )
        return attribute_bonus


# 时节不居
class TimeWaitsforNoOne(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者对我方目标提供治疗时,记录治疗量。当任意我方目标施放攻击后,根据记录治疗量的36%,对随机1个受到攻击的敌方目标造成基于装备者属性的附加伤害
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 棺的回响
class EchoesoftheCoffin(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放终结技后,使我方全体速度提高12点,持续1回合。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            speed_delta = attribute_bonus.get('SpeedDelta', 0)
            attribute_bonus['SpeedDelta'] = (
                speed_delta
                + (
                    weapon_effect['23008']['Param']['speed'][
                        self.weapon_rank - 1
                    ]
                )
            )
        return attribute_bonus


# 惊魂夜
class NightofFright(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者为我方目标提供治疗时,使该目标的攻击力提高2.3%,该效果最多叠加5层
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio
                + (
                    weapon_effect['23017']['Param']['AttackAddedRatio'][
                        self.weapon_rank - 1
                    ]
                )
                * 5
            )
        return attribute_bonus


# 一场术后对话
class PostOpConversation(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 在施放终结技时治疗量提高12%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            Ultra_HealRatioBase = attribute_bonus.get('Ultra_HealRatioBase', 0)
            attribute_bonus['Ultra_HealRatioBase'] = (
                Ultra_HealRatioBase
                + (
                    weapon_effect['21000']['Param']['Ultra_HealRatioBase'][
                        self.weapon_rank - 1
                    ]
                )
            )
        return attribute_bonus


# 同一种心情
class SharedFeeling(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 在施放战技时为我方全体恢复2点能量。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 此时恰好
class PerfectTiming(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者的治疗量提高, 提高数值等同于效果抵抗的33%, 最多使治疗量提高15%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            StatusResistance = attribute_bonus.get('StatusResistance', 0)
            HealRatioBase_maxadd = weapon_effect['21000']['Param'][
                'HealRatioBase'
            ][self.weapon_rank - 1]
            HealRatioBaseadd = (
                StatusResistance
                * weapon_effect['21000']['Param']['StatusResistance'][
                    self.weapon_rank - 1
                ]
            )
            HealRatioBase = attribute_bonus.get('HealRatioBase', 0)
            attribute_bonus['HealRatioBase'] = HealRatioBase + min(
                HealRatioBaseadd, HealRatioBase_maxadd
            )
        return attribute_bonus


# 等价交换
class QuidProQuo(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 随机为1个当前能量百分比小于50%的我方其他目标恢复8点能量。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 暖夜不会漫长
class WarmthShortensColdNights(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 施放普攻或战技后, 为我方全体回复等同于各自生命上限2%的生命值。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 嘿,我在这儿
class HeyOverHere(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放战技时, 治疗量提高16%,持续2回合。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            HealRatioBase = attribute_bonus.get('HealRatioBase', 0)
            attribute_bonus['HealRatioBase'] = (
                HealRatioBase
                + (
                    weapon_effect['22001']['Param']['HealRatioBase'][
                        self.weapon_rank - 1
                    ]
                )
            )
        return attribute_bonus


# 物穰
class Cornucopia(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者施放战技和终结技时, 治疗量提高12%。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            Ultra_HealRatioBase = attribute_bonus.get('Ultra_HealRatioBase', 0)
            attribute_bonus['Ultra_HealRatioBase'] = (
                Ultra_HealRatioBase
                + (
                    weapon_effect['20001']['Param']['HealRatioBase'][
                        self.weapon_rank - 1
                    ]
                )
            )
            BPSkill_HealRatioBase = attribute_bonus.get(
                'BPSkill_HealRatioBase', 0
            )
            attribute_bonus['BPSkill_HealRatioBase'] = (
                BPSkill_HealRatioBase
                + (
                    weapon_effect['20001']['Param']['HealRatioBase'][
                        self.weapon_rank - 1
                    ]
                )
            )
        return attribute_bonus


# 嘉果
class FineFruit(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 战斗开始时, 立即为我方全体恢复6点能量。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 蕃息
class Multiplication(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 战斗开始时, 立即为我方全体恢复6点能量。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 但战斗还未结束
class ButtheBattleIsnotOver(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放战技后, 使下一个行动的我方【其他目标】造成的伤害提高30%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 记忆中的模样
class MemoriesofthePast(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 装备者施放攻击后, 额外恢复4点能量
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 与行星相会
class PlanetaryRendezvous(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当我方目标造成与装备者相同属性的伤害时, 造成的伤害提高12%。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        all_damage_added_ratio = attribute_bonus.get('AllDamageAddedRatio', 0)
        attribute_bonus['AllDamageAddedRatio'] = (
            all_damage_added_ratio
            + (
                weapon_effect['21011']['Param']['AllDamageAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        )
        return attribute_bonus


# 舞! 舞! 舞!
class DanceDanceDance(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放终结技后, 我方全体行动提前16%。
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 过往未来
class PastandFuture(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使下一个行动的我方【其他目标】造成的伤害提高16%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 镂月裁云之意
class CarvetheMoonWeavetheClouds(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 在战斗开始时以及当装备者回合开始时,随机生效1个效果
        # 使我方全体攻击力提高10%
        # 使我方全体暴击伤害提高12%
        # 暂时固定只算攻击
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        AttackAddedRatio = attribute_bonus.get('AttackAddedRatio', 0)
        attribute_bonus['AttackAddedRatio'] = (
            AttackAddedRatio
            + (
                weapon_effect['21032']['Param']['AttackAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        )
        return attribute_bonus


# 齐颂
class Chorus(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 进入战斗后,使我方全体的攻击力提高8%
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        AttackAddedRatio = attribute_bonus.get('AttackAddedRatio', 0)
        attribute_bonus['AttackAddedRatio'] = (
            AttackAddedRatio
            + (
                weapon_effect['20005']['Param']['AttackAddedRatio'][
                    self.weapon_rank - 1
                ]
            )
        )
        return attribute_bonus


# 轮契
class MeshingCogs(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 使装备者施放攻击或受到攻击后,额外恢复4点能量
        pass

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        return attribute_bonus


# 调和
class Mediation(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放终结技后,使我方全体速度提高12点,持续1回合。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            speed_delta = attribute_bonus.get('SpeedDelta', 0)
            attribute_bonus['SpeedDelta'] = (
                speed_delta
                + (
                    weapon_effect['20019']['Param']['speed'][
                        self.weapon_rank - 1
                    ]
                )
            )
        return attribute_bonus

# 嘿，我在这儿
class HeyOverHere(BaseWeapon):
    weapon_base_attributes: Dict

    def __init__(self, weapon: DamageInstanceWeapon):
        super().__init__(weapon)

    async def check(self):
        # 当装备者施放终结技后,使我方全体速度提高12点,持续1回合。
        return True

    async def weapon_ability(
        self,
        Ultra_Use: float,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        if await self.check():
            heal_ratio_base = attribute_bonus.get('HealRatioBase', 0)
            attribute_bonus['HealRatioBase'] = (
                heal_ratio_base
                + (
                    weapon_effect['22001']['Param']['HealRatioBase'][
                        self.weapon_rank - 1
                    ]
                )
            )
        return attribute_bonus

class Weapon:
    @classmethod
    def create(cls, weapon: DamageInstanceWeapon):
        if weapon.id_ == 22001:
            return HeyOverHere(weapon)
        if weapon.id_ == 20019:
            return Mediation(weapon)
        if weapon.id_ == 20012:
            return MeshingCogs(weapon)
        if weapon.id_ == 20005:
            return Chorus(weapon)
        if weapon.id_ == 21032:
            return CarvetheMoonWeavetheClouds(weapon)
        if weapon.id_ == 21025:
            return PastandFuture(weapon)
        if weapon.id_ == 21018:
            return DanceDanceDance(weapon)
        if weapon.id_ == 21011:
            return PlanetaryRendezvous(weapon)
        if weapon.id_ == 21004:
            return MemoriesofthePast(weapon)
        if weapon.id_ == 23003:
            return ButtheBattleIsnotOver(weapon)
        if weapon.id_ == 20015:
            return Multiplication(weapon)
        if weapon.id_ == 20008:
            return FineFruit(weapon)
        if weapon.id_ == 20001:
            return Cornucopia(weapon)
        if weapon.id_ == 22001:
            return HeyOverHere(weapon)
        if weapon.id_ == 21028:
            return WarmthShortensColdNights(weapon)
        if weapon.id_ == 21021:
            return QuidProQuo(weapon)
        if weapon.id_ == 21014:
            return PerfectTiming(weapon)
        if weapon.id_ == 21007:
            return SharedFeeling(weapon)
        if weapon.id_ == 21000:
            return PostOpConversation(weapon)
        if weapon.id_ == 23017:
            return NightofFright(weapon)
        if weapon.id_ == 23008:
            return EchoesoftheCoffin(weapon)
        if weapon.id_ == 23013:
            return TimeWaitsforNoOne(weapon)
        if weapon.id_ == 23018:
            return AnInstanceBeforeAGaze(weapon)
        if weapon.id_ == 23016:
            return WorrisomeBlissf(weapon)
        if weapon.id_ == 23012:
            return SleepLiketheDead(weapon)
        if weapon.id_ == 23014:
            return Thisbodyisasword(weapon)
        if weapon.id_ == 20006:
            return DataBank(weapon)
        if weapon.id_ == 20013:
            return Passkey(weapon)
        if weapon.id_ == 20020:
            return Sagacity(weapon)
        if weapon.id_ == 20004:
            return Void(weapon)
        if weapon.id_ == 20011:
            return Loop(weapon)
        if weapon.id_ == 20018:
            return HiddenShadow(weapon)
        if weapon.id_ == 20002:
            return CollapsingSky(weapon)
        if weapon.id_ == 20009:
            return ShatteredHome(weapon)
        if weapon.id_ == 20016:
            return MutualDemise(weapon)
        if weapon.id_ == 20003:
            return Amber(weapon)
        if weapon.id_ == 20010:
            return Defense(weapon)
        if weapon.id_ == 20017:
            return Pioneering(weapon)
        if weapon.id_ == 21002:
            return DayOneofMyNewLife(weapon)
        if weapon.id_ == 21009:
            return LandausChoice(weapon)
        if weapon.id_ == 21016:
            return TrendoftheUniversalMarket(weapon)
        if weapon.id_ == 21023:
            return WeAreWildfire(weapon)
        if weapon.id_ == 21030:
            return ThisIsMe(weapon)
        if weapon.id_ == 24002:
            return TextureofMemories(weapon)
        if weapon.id_ == 23005:
            return MomentofVictory(weapon)
        if weapon.id_ == 23011:
            return SheAlreadyShutHerEyes(weapon)
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
