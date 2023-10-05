from collections import Counter
from typing import Dict, List, Union

from gsuid_core.logger import logger

from ..utils import merge_attribute
from ..Base.model import DamageInstanceRelic
from ..Base.RelicBase import SingleRelic, BaseRelicSetSkill


class Relic101(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        在战斗开始时
        """
        logger.info('Relic101 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            pass
        return attribute_bonus


class Relic102(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        无
        """
        logger.info('Relic102 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            a_dmg = attribute_bonus.get('NormalDmgAdd', 0)
            attribute_bonus['NormalDmgAdd'] = a_dmg + 0.10000000018626451
        return attribute_bonus


class Relic103(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        战斗中生效:装备者提供的护盾量提高
        """
        logger.info('Relic103 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            shield_added_ratio = attribute_bonus.get('shield_added_ratio', 0)
            attribute_bonus['shield_added_ratio'] = (
                shield_added_ratio + 0.20000000018626451
            )
        return attribute_bonus


class Relic104(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者施放终结技
        """
        logger.info('Relic104 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            critical_damage_base = attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus['CriticalDamageBase'] = (
                critical_damage_base + 0.25000000023283064
            )
        return attribute_bonus


class Relic105(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        施放攻击或受到攻击时, 默认叠满
        """
        logger.info('Relic105 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio + 0.05000000004656613 * 5
            )
        return attribute_bonus


class Relic106(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        无
        """
        logger.info('Relic106 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            pass
        return attribute_bonus


class Relic107(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        TODO: 检查是否是火属性伤害
        """
        logger.info('Relic107 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4:
            e_dmg = attribute_bonus.get('BPSkillDmgAdd', 0)
            attribute_bonus['BPSkillDmgAdd'] = e_dmg + 0.12000000011175871
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            fire_added_ratio = attribute_bonus.get('FireAddedRatio', 0)
            attribute_bonus['FireAddedRatio'] = (
                fire_added_ratio + 0.12000000011175871
            )
        return attribute_bonus


class Relic108(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者对敌方目标造成伤害
        目标拥有量子属性弱点
        """
        logger.info('Relic108 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info(attribute_bonus)
            ignore_defence = attribute_bonus.get('ignore_defence', 0)
            attribute_bonus['ignore_defence'] = (
                ignore_defence + 0.10000000009313226 * 2
            )
        return attribute_bonus


class Relic109(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        TODO: 检查是否释放战技
        """
        logger.info('Relic109 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info(attribute_bonus)
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio + 0.20000000018626451
            )
        return attribute_bonus


class Relic110(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者施放终结技
        """
        logger.info('Relic110 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('ModifyActionDelay')
        return attribute_bonus


class Relic111(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)
        self._count = count

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者击破敌方目标弱点
        """
        logger.info('Relic111 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('ModifySPNew')
        return attribute_bonus


class Relic112(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)
        self._count = count

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者对陷入负面效果的敌方目标造成伤害
        对陷入禁锢状态的敌方目标造成伤害
        """
        logger.info('Relic111 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('对陷入负面效果的敌方目标造成伤害')
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus['CriticalChanceBase'] = (
                critical_chance_base + 0.10000000009313226
            )
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('对陷入禁锢状态的敌方目标造成伤害')
            critical_damage_base = attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus['CriticalDamageBase'] = (
                critical_damage_base + 0.20000000018626451
            )
        return attribute_bonus


class Relic113(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)
        self._count = count

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        当装备者受到攻击或被我方目标消耗生命值后, 暴击率提高8%, 持续2回合, 该效果最多叠加2层。
        """
        logger.info('Relic113 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('当装备者受到攻击或被我方目标消耗生命值后')
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus['CriticalChanceBase'] = (
                critical_chance_base + 0.08000000009313226 * 2
            )
        return attribute_bonus


class Relic114(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)
        self._count = count

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        当装备者对我方目标施放终结技时, 我方全体速度提高12%, 持续1回合, 该效果无法叠加。
        """
        logger.info('Relic114 check success')
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            speed_added_ratio = attribute_bonus.get('SpeedAddedRatio', 0)
            attribute_bonus['SpeedAddedRatio'] = (
                speed_added_ratio + 0.12000000011175871
            )
        return attribute_bonus


class Relic301(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者的速度大于等于120
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['speed'] >= 120:
            logger.info('Relic306 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio + 0.12000000011175871
            )
        return attribute_bonus


class Relic302(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者的速度大于等于120
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['speed'] >= 120:
            logger.info('Relic306 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio + 0.0800000000745058
            )
        return attribute_bonus


class Relic303(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        # 提高装备者等同于当前效果命中25%的攻击力,最多提高25%
        return True

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            merged_attr = await merge_attribute(base_attr, attribute_bonus)
            status_probability = merged_attr.get('StatusProbabilityBase', 0)
            # 提高装备者等同于当前效果命中25%的攻击力,最多提高25%
            attribute_bonus['AttackAddedRatio'] = attack_added_ratio + min(
                0.25000000023283064, status_probability / 0.25
            )
        return attribute_bonus


class Relic304(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        备者的效果命中大于等于50%
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['StatusResistanceBase'] >= 0.5000000004656613:
            logger.info('Relic306 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            defence_added_ratio = attribute_bonus.get('DefenceAddedRatio', 0)
            attribute_bonus['DefenceAddedRatio'] = (
                defence_added_ratio + 0.1500000001396984
            )
        return attribute_bonus


class Relic305(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者的暴击伤害大于等于120%
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['CriticalDamageBase'] >= 1.2000000001862645:
            logger.info('Relic306 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus['CriticalChanceBase'] = (
                critical_chance_base + 0.6000000005587935
            )
        return attribute_bonus


class Relic306(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者当前暴击率大于等于50%
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['CriticalChanceBase'] >= 0.5:
            logger.info('Relic306 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            q_dmg = attribute_bonus.get('UltraDmgAdd', 0)
            attribute_bonus['UltraDmgAdd'] = q_dmg + 0.1500000001396984
            a3_dmg = attribute_bonus.get('TalentDmgAdd', 0)
            attribute_bonus['TalentDmgAdd'] = a3_dmg + 0.1500000001396984
        return attribute_bonus


class Relic307(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者的速度大于等于145
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['speed'] >= 145:
            logger.info('Relic306 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            break_damage_added_ratio_base = attribute_bonus.get(
                'BreakDamageAddedRatioBase', 0
            )
            attribute_bonus['BreakDamageAddedRatioBase'] = (
                break_damage_added_ratio_base + 0.20000000018626451
            )
        return attribute_bonus


class Relic308(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        装备者的速度大于等于120
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['speed'] >= 120:
            logger.info('Relic306 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            logger.info('ModifyActionDelay')
        return attribute_bonus


class Relic309(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        当装备者的当前暴击率大于等于70%时, 普攻和战技造成的伤害提高20%。
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['CriticalChanceBase'] >= 0.7:
            logger.info('Relic309 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            a_dmg = attribute_bonus.get('NormalDmgAdd', 0)
            attribute_bonus['NormalDmgAdd'] = a_dmg + 0.20000000018626451
            a2_dmg = attribute_bonus.get('BPSkillDmgAdd', 0)
            attribute_bonus['BPSkillDmgAdd'] = a2_dmg + 0.20000000018626451
        return attribute_bonus


class Relic310(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        """
        当装备者的效果抵抗大于等于30%时, 我方全体暴击伤害提高10%。
        """
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['StatusResistanceBase'] >= 0.3:
            logger.info('Relic310 check success')
            return True
        return False

    async def set_skill_ability(
        self, base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
    ):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            critical_damage_base = attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus['CriticalDamageBase'] = (
                critical_damage_base + 0.10000000018626451
            )
        return attribute_bonus


class RelicSet:
    HEAD: SingleRelic
    HAND: SingleRelic
    BODY: SingleRelic
    FOOT: SingleRelic
    NECK: SingleRelic
    OBJECT: SingleRelic
    Unknow: SingleRelic

    SetSkill: List[
        Union[
            Relic101,
            Relic102,
            Relic103,
            Relic104,
            Relic105,
            Relic106,
            Relic107,
            Relic108,
            Relic109,
            Relic110,
            Relic111,
            Relic112,
            Relic113,
            Relic114,
            Relic301,
            Relic302,
            Relic303,
            Relic304,
            Relic305,
            Relic306,
            Relic307,
            Relic308,
            Relic309,
            Relic310,
        ]
    ]

    def create(self, relic_list: List[DamageInstanceRelic]):
        set_id_list: List[int] = []
        for relic in relic_list:
            set_id_list.append(relic.SetId)

            if relic.Type == 1:
                self.HEAD = SingleRelic(relic)
            elif relic.Type == 2:
                self.HAND = SingleRelic(relic)
            elif relic.Type == 3:
                self.BODY = SingleRelic(relic)
            elif relic.Type == 4:
                self.FOOT = SingleRelic(relic)
            elif relic.Type == 5:
                self.NECK = SingleRelic(relic)
            elif relic.Type == 6:
                self.OBJECT = SingleRelic(relic)
            else:
                self.Unknow = SingleRelic(relic)

        self.set_id_counter = Counter(set_id_list).most_common()
        self.check_set()
        self.get_attribute()
        return self

    def get_attribute(self):
        for item in self.__dict__:
            if type(self.__dict__[item]) == SingleRelic:
                itme__: SingleRelic = self.__dict__[item]
                itme__.get_attribute_()

    def check_set(self):
        self.SetSkill = []
        for item in self.set_id_counter:
            set_id = item[0]
            count = item[1]

            if set_id == 101:
                self.SetSkill.append(Relic101(set_id, count))
            elif set_id == 102:
                self.SetSkill.append(Relic102(set_id, count))
            elif set_id == 103:
                self.SetSkill.append(Relic103(set_id, count))
            elif set_id == 104:
                self.SetSkill.append(Relic104(set_id, count))
            elif set_id == 105:
                self.SetSkill.append(Relic105(set_id, count))
            elif set_id == 106:
                self.SetSkill.append(Relic106(set_id, count))
            elif set_id == 107:
                self.SetSkill.append(Relic107(set_id, count))
            elif set_id == 108:
                self.SetSkill.append(Relic108(set_id, count))
            elif set_id == 109:
                self.SetSkill.append(Relic109(set_id, count))
            elif set_id == 110:
                self.SetSkill.append(Relic110(set_id, count))
            elif set_id == 111:
                self.SetSkill.append(Relic111(set_id, count))
            elif set_id == 112:
                self.SetSkill.append(Relic112(set_id, count))
            elif set_id == 113:
                self.SetSkill.append(Relic113(set_id, count))
            elif set_id == 114:
                self.SetSkill.append(Relic114(set_id, count))
            elif set_id == 301:
                self.SetSkill.append(Relic301(set_id, count))
            elif set_id == 302:
                self.SetSkill.append(Relic302(set_id, count))
            elif set_id == 303:
                self.SetSkill.append(Relic303(set_id, count))
            elif set_id == 304:
                self.SetSkill.append(Relic304(set_id, count))
            elif set_id == 305:
                self.SetSkill.append(Relic305(set_id, count))
            elif set_id == 306:
                self.SetSkill.append(Relic306(set_id, count))
            elif set_id == 307:
                self.SetSkill.append(Relic307(set_id, count))
            elif set_id == 308:
                self.SetSkill.append(Relic308(set_id, count))
            elif set_id == 309:
                self.SetSkill.append(Relic309(set_id, count))
            elif set_id == 310:
                self.SetSkill.append(Relic310(set_id, count))
            else:
                raise Exception(f'Unknow SetId: {set_id}')
