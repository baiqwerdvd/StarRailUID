from typing import Dict

from .Avatar import Avatar
from .Weapon import Weapon
from .Relic import RelicSet, SingleRelic


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
        print(self.base_attr)

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
        print(self.attribute_bonus)
