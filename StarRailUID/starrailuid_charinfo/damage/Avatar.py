import json
from pathlib import Path

from gsuid_core.logger import logger

from .Weapon.Weapon import Weapon
from ..mono.Character import Character
from .Base.model import DamageInstance
from .Base.AvatarBase import BaseAvatarinfo
from .Relic.Relic import RelicSet, SingleRelic
from .AvatarDamage.AvatarDamage import AvatarDamage

Excel_path = Path(__file__).parent
with Path.open(Excel_path / 'Excel' / 'SkillData.json', encoding='utf-8') as f:
    skill_dict = json.load(f)


class AvatarInstance:
    def __init__(self, raw_data: Character):
        self.raw_data = DamageInstance(raw_data)
        self.avatardamage = AvatarDamage.create(
            self.raw_data.avatar, self.raw_data.skill
        )
        self.avatar = BaseAvatarinfo(self.raw_data.avatar)
        self.weapon = Weapon.create(self.raw_data.weapon)
        self.relic_set = RelicSet().create(self.raw_data.relic)

        self.base_attr = self.cal_role_base_attr()
        self.attribute_bonus: dict[str, float] = {}

        self.cal_relic_attr_add()
        self.cal_avatar_attr_add()
        self.cal_avatar_eidolon_add()
        self.cal_weapon_attr_add()

    def cal_role_base_attr(self):
        logger.info('cal_role_base_attr')
        base_attr: dict[str, float] = {}
        avatar_attribute = self.avatar.avatar_attribute
        for attr_name, attr_value in avatar_attribute.items():
            if attr_name in base_attr:
                base_attr[attr_name] += attr_value
            else:
                base_attr[attr_name] = attr_value

        weapon_attribute = self.weapon.weapon_base_attribute
        for attr_name, attr_value in weapon_attribute.items():
            if attr_name in base_attr:
                base_attr[attr_name] += attr_value
            else:
                base_attr[attr_name] = attr_value
        return base_attr

    def cal_relic_attr_add(self):
        # 单件属性
        for relic_type in self.relic_set.__dict__:
            if type(self.relic_set.__dict__[relic_type]) == SingleRelic:
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

        # 套装面板加成属性
        for set_skill in self.relic_set.SetSkill:
            for attribute in set_skill.relicSetAttribute:
                if attribute in self.attribute_bonus:
                    self.attribute_bonus[
                        attribute
                    ] += set_skill.relicSetAttribute[attribute]
                else:
                    self.attribute_bonus[
                        attribute
                    ] = set_skill.relicSetAttribute[attribute]

    def cal_avatar_eidolon_add(self):
        for attribute in self.avatardamage.eidolon_attribute:
            if attribute in self.attribute_bonus:
                self.attribute_bonus[
                    attribute
                ] += self.avatardamage.eidolon_attribute[attribute]
            else:
                self.attribute_bonus[
                    attribute
                ] = self.avatardamage.eidolon_attribute[attribute]
        for attribute in self.avatardamage.extra_ability_attribute:
            if attribute in self.attribute_bonus:
                self.attribute_bonus[
                    attribute
                ] += self.avatardamage.extra_ability_attribute[attribute]
            else:
                self.attribute_bonus[
                    attribute
                ] = self.avatardamage.extra_ability_attribute[attribute]

    def cal_avatar_attr_add(self):
        attribute_bonus = self.avatar.avatar_attribute_bonus
        if attribute_bonus:
            for bonus in attribute_bonus:
                status_add = bonus.statusAdd
                bonus_property = status_add.property
                value = status_add.value
                if bonus_property in self.attribute_bonus:
                    self.attribute_bonus[bonus_property] += value
                else:
                    self.attribute_bonus[bonus_property] = value

    def cal_weapon_attr_add(self):
        for attribute in self.weapon.weapon_attribute:
            if attribute in self.attribute_bonus:
                self.attribute_bonus[
                    attribute
                ] += self.weapon.weapon_attribute[attribute]
            else:
                self.attribute_bonus[attribute] = self.weapon.weapon_attribute[
                    attribute
                ]

    async def gat_damage(self):
        logger.info('base_attr')
        logger.info(self.base_attr)
        logger.info('attribute_bonus')
        logger.info(self.attribute_bonus)

        logger.info('检查武器战斗生效的buff')
        Ultra_Use = self.avatar.Ultra_Use()
        logger.info('Ultra_Use')
        logger.info(Ultra_Use)
        self.attribute_bonus = await self.weapon.weapon_ability(
            Ultra_Use, self.base_attr, self.attribute_bonus
        )
        logger.info(self.attribute_bonus)
        logger.info('检查遗器套装战斗生效的buff')
        for set_skill in self.relic_set.SetSkill:
            self.attribute_bonus = await set_skill.set_skill_ability(
                self.base_attr, self.attribute_bonus
            )
        if self.attribute_bonus is None:
            raise Exception('attribute_bonus is None')
        logger.info(self.attribute_bonus)

        return await self.avatardamage.getdamage(
            self.base_attr, self.attribute_bonus
        )
