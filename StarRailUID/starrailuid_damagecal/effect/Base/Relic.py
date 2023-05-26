from typing import Dict, List
from abc import abstractmethod
from collections import Counter

from mpmath import mp

mp.dps = 14


class SingleRelic:
    def __init__(self, relic: Dict):
        self.raw_relic = relic
        self.relic_id = relic['relicId']
        self.set_id = relic['SetId']
        self.relic_type = relic['Type']
        self.relic_level = relic.get('Level', 0)
        self.relic_attribute_bonus = {}

    async def get_attribute_(self):
        # MainAffix
        self.relic_attribute_bonus[
            self.raw_relic['MainAffix']['Property']
        ] = mp.mpf(self.raw_relic['MainAffix']['Value'])

        # SubAffix
        if self.raw_relic.get('SubAffixList'):
            for sub_affix in self.raw_relic['SubAffixList']:
                sub_affix_property = sub_affix['Property']
                value = mp.mpf(sub_affix['Value'])
                if sub_affix_property in self.relic_attribute_bonus:
                    self.relic_attribute_bonus[sub_affix_property] += value
                else:
                    self.relic_attribute_bonus[sub_affix_property] = value


class BaseRelicSetSkill:
    @abstractmethod
    async def check(self):
        ...

    @abstractmethod
    async def set_skill_ability(self, char):
        '''
        战斗加成属性, 与 set_skill_property() 互斥
        '''
        ...

    @abstractmethod
    async def set_skill_property_ability(self, char):
        '''
        面板加成属性, 与 set_skill_ability_param() 互斥
        '''
        ...


class Relic108(BaseRelicSetSkill):
    async def check(self):
        pass

    async def set_skill_ability(self, char):
        pass

    async def set_skill_property_ability(self, char):
        pass


class Relic306(BaseRelicSetSkill):
    async def check(self):
        pass

    async def set_skill_ability(self, char):
        pass

    async def set_skill_property_ability(self, char):
        pass


class RelicSet:
    HEAD: SingleRelic
    HAND: SingleRelic
    BODY: SingleRelic
    FOOT: SingleRelic
    NECK: SingleRelic
    OBJECT: SingleRelic
    Unknow: SingleRelic

    set_id_counter: List
    SetSkill: List = []

    def __init__(self, relic_list: List):
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

    async def get_attribute(self):
        for item in self.__dict__:
            if type(self.__dict__[item]) != SingleRelic:
                break
            await self.__dict__[item].get_attribute_()

    async def check_set(self):
        for item in self.set_id_counter:
            set_id = item[0]
            count = item[1]
            if count == 1:
                break
            if set_id == 108:
                self.SetSkill.append(Relic108())
            if set_id == 306:
                self.SetSkill.append(Relic306())
