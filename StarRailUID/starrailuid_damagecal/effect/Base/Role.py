from typing import Dict

from mpmath import mp

from .Avatar import Avatar
from .Weapon import Weapon
from .Relic import RelicSet, SingleRelic

mp.dps = 14


class RoleInstance:
    def __init__(self, raw_data: Dict):
        self.raw_data = raw_data

        self.avatar = Avatar(raw_data['avatar'])
        self.weapon = Weapon(raw_data['weapon'])
        self.relic_set = RelicSet(raw_data['relic'])

        self.base_attr = {}
        self.attribute_bonus = {}

    async def cal_role_base_attr(self):
        await self.avatar.get_attribute()
        avatar_attribute = self.avatar.__dict__['avatar_attribute']
        for attribute in avatar_attribute:
            if attribute in self.base_attr:
                self.base_attr[attribute] += avatar_attribute[attribute]
            else:
                self.base_attr[attribute] = avatar_attribute[attribute]

        await self.weapon.get_attribute()
        weapon_attribute = self.weapon.__dict__['weapon_attribute']
        for attribute in weapon_attribute:
            if attribute in self.base_attr:
                self.base_attr[attribute] += weapon_attribute[attribute]
            else:
                self.base_attr[attribute] = weapon_attribute[attribute]

    async def cal_relic_attr_add(self):
        await self.relic_set.get_attribute()
        for relic_type in self.relic_set.__dict__:
            if type(self.relic_set.__dict__[relic_type]) != SingleRelic:
                break
            relic: SingleRelic = self.relic_set.__dict__[relic_type]
            for attribute in relic.relic_attribute_bonus:
                if attribute in self.attribute_bonus:
                    self.attribute_bonus[
                        attribute
                    ] += relic.relic_attribute_bonus[attribute]
                else:
                    self.attribute_bonus[
                        attribute
                    ] = relic.relic_attribute_bonus[attribute]

    async def cal_avatar_attr_add(self):
        attribute_bonus = self.avatar.avatar_attribute_bonus
        for bonus in attribute_bonus:
            status_add = bonus['statusAdd']
            bonus_property = status_add['property']
            value = mp.mpf(status_add['value'])
            if bonus_property in self.attribute_bonus:
                self.attribute_bonus[bonus_property] += value
            else:
                self.attribute_bonus[bonus_property] = value
