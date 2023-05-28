from typing import Dict, List
from collections import Counter

from mpmath import mp
from gsuid_core.logger import logger

from ..utils import merge_attribute
from ..Base.RelicBase import SingleRelic, BaseRelicSetSkill


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

    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        if self.pieces2 and await self.check(base_attr, attribute_bonus):
            q_dmg = attribute_bonus.get('UltraDmgAdd', 0)
            attribute_bonus['UltraDmgAdd'] = q_dmg + mp.mpf(0.1500000001396984)
            a3_dmg = attribute_bonus.get('Follow-UpAttackDmgAdd', 0)
            attribute_bonus['Follow-UpDmgAdd'] = a3_dmg + mp.mpf(
                0.1500000001396984
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
            if count == 1:
                break
            if set_id == 108:
                self.SetSkill.append(Relic108(set_id, count))
            if set_id == 306:
                self.SetSkill.append(Relic306(set_id, count))
