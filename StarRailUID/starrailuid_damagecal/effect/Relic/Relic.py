from collections import Counter
from typing import Dict, List

from mpmath import mp

from gsuid_core.logger import logger

from ..Base.RelicBase import BaseRelicSetSkill, SingleRelic
from ..utils import merge_attribute


class Relic101(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        在战斗开始时
        '''
        logger.info('Relic101 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            pass
        return attribute_bonus


class Relic102(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        无
        '''
        logger.info('Relic102 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            pass
        return attribute_bonus


class Relic103(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        战斗中生效:装备者提供的护盾量提高
        '''
        logger.info('Relic103 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            shield_added_ratio = attribute_bonus.get('shield_added_ratio', 0)
            attribute_bonus[
                'shield_added_ratio'
            ] = shield_added_ratio + mp.mpf(0.20000000018626451)
        return attribute_bonus


class Relic104(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者施放终结技
        '''
        logger.info('Relic104 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            critical_damage_base = attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus[
                'CriticalDamageBase'
            ] = critical_damage_base + mp.mpf(0.25000000023283064)
        return attribute_bonus


class Relic105(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        施放攻击或受到攻击时, 默认叠满
        '''
        logger.info('Relic105 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = (
                attack_added_ratio + mp.mpf(0.05000000004656613) * 5
            )
        return attribute_bonus


class Relic106(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        无
        '''
        logger.info('Relic106 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            pass
        return attribute_bonus


class Relic107(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        TODO: 检查是否是火属性伤害
        '''
        logger.info('Relic107 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4:
            e_dmg = attribute_bonus.get('BPSkillDmgAdd', {})
            q_dmg = attribute_bonus.get('UltraSkillDmgAdd', {})
            attribute_bonus['BPSkillDmgAdd'] = e_dmg + mp.mpf(
                0.12000000011175871
            )
            attribute_bonus['UltraSkillDmgAdd'] = q_dmg + mp.mpf(
                0.12000000011175871
            )
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            fire_added_ratio = attribute_bonus.get('FireAddedRatio', {})
            attribute_bonus['FireAddedRatio'] = fire_added_ratio + mp.mpf(
                0.12000000011175871
            )
        return attribute_bonus


class Relic108(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者对敌方目标造成伤害
        目标拥有量子属性弱点
        '''
        logger.info('Relic108 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            ignore_defence = attribute_bonus.get('ignore_defence', 0)
            attribute_bonus['ignore_defence'] = (
                ignore_defence + mp.mpf(0.10000000009313226) * 2
            )
        return attribute_bonus


class Relic109(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        TODO: 检查是否释放战技
        '''
        logger.info('Relic109 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
                0.20000000018626451
            )
        return attribute_bonus


class Relic110(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者施放终结技
        '''
        logger.info('Relic110 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('ModifyActionDelay')
            pass
        return attribute_bonus


class Relic111(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)
        self._count = count

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者击破敌方目标弱点
        '''
        logger.info('Relic111 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('ModifySPNew')
            pass
        return attribute_bonus


class Relic112(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)
        self._count = count

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者对陷入负面效果的敌方目标造成伤害
        对陷入禁锢状态的敌方目标造成伤害
        '''
        logger.info('Relic111 check success')
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('对陷入负面效果的敌方目标造成伤害')
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus[
                'CriticalChanceBase'
            ] = critical_chance_base + mp.mpf(0.10000000009313226)
        if self.pieces4 and await self.check(base_attr, attribute_bonus):
            logger.info('对陷入禁锢状态的敌方目标造成伤害')
            critical_damage_base = attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus[
                'CriticalDamageBase'
            ] = critical_damage_base + mp.mpf(0.20000000018626451)
        return attribute_bonus


class Relic301(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者的速度大于等于120
        '''
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['speed'] >= mp.mpf(120):
            logger.info('Relic306 check success')
            return True
        return None

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
                0.12000000011175871
            )
        return attribute_bonus


class Relic302(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者的速度大于等于120
        '''
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['speed'] >= mp.mpf(120):
            logger.info('Relic306 check success')
            return True
        return None

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            attribute_bonus['AttackAddedRatio'] = attack_added_ratio + mp.mpf(
                0.0800000000745058
            )
        return attribute_bonus


class Relic303(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        pass
        return True

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
            merged_attr = await merge_attribute(base_attr, attribute_bonus)
            status_probability = merged_attr.get('StatusProbability', 0)
            # 提高装备者等同于当前效果命中25%的攻击力,最多提高25%
            attribute_bonus['AttackAddedRatio'] = attack_added_ratio + min(
                mp.mpf(0.25000000023283064), status_probability / mp.mpf(0.25)
            )
        return attribute_bonus


class Relic304(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        备者的效果命中大于等于50%
        '''
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['StatusProbability'] >= mp.mpf(0.5000000004656613):
            logger.info('Relic306 check success')
            return True
        return None

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            defence_added_ratio = attribute_bonus.get('DefenceAddedRatio', 0)
            attribute_bonus[
                'DefenceAddedRatio'
            ] = defence_added_ratio + mp.mpf(0.1500000001396984)
        return attribute_bonus


class Relic305(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者的暴击伤害大于等于120%
        '''
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['CriticalDamageBase'] >= mp.mpf(1.2000000001862645):
            logger.info('Relic306 check success')
            return True
        return None

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            critical_chance_base = attribute_bonus.get('CriticalChanceBase', 0)
            attribute_bonus[
                'CriticalChanceBase'
            ] = critical_chance_base + mp.mpf(0.6000000005587935)
        return attribute_bonus


class Relic306(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者当前暴击率大于等于50%
        '''
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['CriticalChanceBase'] >= mp.mpf(0.5):
            logger.info('Relic306 check success')
            return True
        return None

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            q_dmg = attribute_bonus.get('UltraDmgAdd', 0)
            attribute_bonus['UltraDmgAdd'] = q_dmg + mp.mpf(0.1500000001396984)
            a3_dmg = attribute_bonus.get('Follow-UpAttackDmgAdd', 0)
            attribute_bonus['Follow-UpDmgAdd'] = a3_dmg + mp.mpf(
                0.1500000001396984
            )
        return attribute_bonus


class Relic307(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者的速度大于等于145
        '''
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['speed'] >= mp.mpf(145):
            logger.info('Relic306 check success')
            return True
        return None

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            break_damage_added_ratio_base = attribute_bonus.get(
                'BreakDamageAddedRatioBase', 0
            )
            attribute_bonus[
                'BreakDamageAddedRatioBase'
            ] = break_damage_added_ratio_base + mp.mpf(0.20000000018626451)
        return attribute_bonus


class Relic308(BaseRelicSetSkill):
    def __init__(self, set_id: int, count: int):
        super().__init__(set_id, count)

    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        装备者的速度大于等于120
        '''
        merged_attr = await merge_attribute(base_attr, attribute_bonus)
        if merged_attr['speed'] >= mp.mpf(120):
            logger.info('Relic306 check success')
            return True
        return None

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            logger.info('ModifyActionDelay')
        return attribute_bonus


class RelicSet:
    HEAD: SingleRelic
    HAND: SingleRelic
    BODY: SingleRelic
    FOOT: SingleRelic
    NECK: SingleRelic
    OBJECT: SingleRelic
    Unknow: SingleRelic

    set_id_counter: List = []
    SetSkill: List

    def __init__(self, relic_list: List):
        self.SetSkill = []
        set_id_list = []
        for relic in relic_list:
            set_id_list.append(relic['SetId'])

            if relic['Type'] == 1:
                self.HEAD = SingleRelic(relic)
            elif relic['Type'] == 2:
                self.HAND = SingleRelic(relic)
            elif relic['Type'] == 3:
                self.BODY = SingleRelic(relic)
            elif relic['Type'] == 4:
                self.FOOT = SingleRelic(relic)
            elif relic['Type'] == 5:
                self.NECK = SingleRelic(relic)
            elif relic['Type'] == 6:
                self.OBJECT = SingleRelic(relic)
            else:
                self.Unknow = SingleRelic(relic)

        self.set_id_counter: List = Counter(set_id_list).most_common()
        self.check_set()
        self.get_attribute()

    def get_attribute(self):
        for item in self.__dict__:
            if type(self.__dict__[item]) == SingleRelic:
                self.__dict__[item].get_attribute_()

    def check_set(self):
        for item in self.set_id_counter:
            set_id = item[0]
            count = item[1]
            # if count == 1:
            #     break
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
            else:
                raise Exception(f'Unknow SetId: {set_id}')
