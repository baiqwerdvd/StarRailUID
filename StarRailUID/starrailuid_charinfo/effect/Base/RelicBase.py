from typing import Dict
from abc import abstractmethod

from mpmath import mp
from gsuid_core.logger import logger

from .model import DamageInstanceRelic
from ....utils.map.SR_MAP_PATH import RelicSetSkill

mp.dps = 14


class SingleRelic:
    def __init__(self, relic: DamageInstanceRelic):
        self.raw_relic = relic
        self.relic_id = relic.relicId
        self.set_id = relic.SetId
        self.relic_type = relic.Type
        self.relic_level = relic.Level
        self.relic_attribute_bonus = {}

    def get_attribute_(self):
        # MainAffix
        if self.raw_relic.MainAffix.Property in self.relic_attribute_bonus:
            self.relic_attribute_bonus[
                self.raw_relic.MainAffix.Property
            ] += mp.mpf(self.raw_relic.MainAffix.Value)
        else:
            self.relic_attribute_bonus[
                self.raw_relic.MainAffix.Property
            ] = mp.mpf(self.raw_relic.MainAffix.Value)

        # SubAffix
        if self.raw_relic.SubAffixList:
            for sub_affix in self.raw_relic.SubAffixList:
                sub_affix_property = sub_affix.Property
                value = mp.mpf(sub_affix.Value)
                if sub_affix_property in self.relic_attribute_bonus:
                    self.relic_attribute_bonus[sub_affix_property] += value
                else:
                    self.relic_attribute_bonus[sub_affix_property] = value


class BaseRelicSetSkill:
    setId: int
    pieces2: bool = False
    pieces4: bool = False

    def __init__(self, set_id: int, count: int):
        self.setId = set_id
        if count >= 2:
            self.pieces2 = True
            logger.info(f'Relic {set_id} 2 pieces set activated')
        if count == 4:
            self.pieces4 = True
            logger.info(f'Relic {set_id} 4 pieces set activated')
        self.relicSetAttribute = {}
        self.set_skill_property_ability()

    @abstractmethod
    async def check(self, base_attr: Dict, attribute_bonus: Dict):
        ...

    @abstractmethod
    async def set_skill_ability(self, base_attr: Dict, attribute_bonus: Dict):
        '''
        战斗加成属性, 与 set_skill_property() 互斥
        '''
        ...

    def set_skill_property_ability(self):
        set_property = ''
        set_value = mp.mpf(0)
        if self.pieces2 and RelicSetSkill[str(self.setId)]['2'] != {}:
            set_property = RelicSetSkill[str(self.setId)]['2']['Property']
            set_value = mp.mpf(RelicSetSkill[str(self.setId)]['2']['Value'])
        if self.pieces4 and RelicSetSkill[str(self.setId)]['4'] != {}:
            set_property = RelicSetSkill[str(self.setId)]['4']['Property']
            set_value = mp.mpf(RelicSetSkill[str(self.setId)]['4']['Value'])
        if set_property != '':
            if set_property in self.relicSetAttribute:
                self.relicSetAttribute[set_property] = (
                    self.relicSetAttribute[set_property] + set_value
                )
            else:
                self.relicSetAttribute[set_property] = set_value
