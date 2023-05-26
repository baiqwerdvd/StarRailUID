from typing import Dict, List
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


class RelicSet:
    HEAD: SingleRelic
    HAND: SingleRelic
    BODY: SingleRelic
    FOOT: SingleRelic
    NECK: SingleRelic
    OBJECT: SingleRelic
    Unknow: SingleRelic

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
        for relic in self.__dict__:
            if relic == 'set_id_counter':
                break
            await self.__dict__[relic].get_attribute_()
