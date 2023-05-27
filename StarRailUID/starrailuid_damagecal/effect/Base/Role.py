from typing import Dict

from mpmath import mp
from gsuid_core.logger import logger

from .Avatar import Avatar
from .Weapon import Weapon
from .utils import merge_attribute
from .Relic import RelicSet, SingleRelic

mp.dps = 14


class RoleInstance:
    def __init__(self, raw_data: Dict):
        self.raw_data = raw_data

        self.avatar = Avatar(raw_data['avatar'], raw_data['skill'])
        self.weapon = Weapon(raw_data['weapon'])
        self.relic_set = RelicSet(raw_data['relic'])

        self.base_attr = {}
        self.attribute_bonus = {}

        self.cal_role_base_attr()
        self.cal_relic_attr_add()
        self.cal_avatar_attr_add()
        self.cal_avatar_eidolon_add()
        self.cal_weapon_attr_add()

    def cal_role_base_attr(self):
        self.avatar.get_attribute()
        avatar_attribute = self.avatar.__dict__['avatar_attribute']
        for attribute in avatar_attribute:
            if attribute in self.base_attr:
                self.base_attr[attribute] += avatar_attribute[attribute]
            else:
                self.base_attr[attribute] = avatar_attribute[attribute]

        self.weapon.get_attribute()
        weapon_attribute = self.weapon.__dict__['weapon_base_attribute']
        for attribute in weapon_attribute:
            if attribute in self.base_attr:
                self.base_attr[attribute] += weapon_attribute[attribute]
            else:
                self.base_attr[attribute] = weapon_attribute[attribute]

    def cal_relic_attr_add(self):
        # 单件属性
        self.relic_set.get_attribute()
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

    def cal_avatar_attr_add(self):
        attribute_bonus = self.avatar.avatar_attribute_bonus
        for bonus in attribute_bonus:
            status_add = bonus['statusAdd']
            bonus_property = status_add['property']
            value = mp.mpf(status_add['value'])
            if bonus_property in self.attribute_bonus:
                self.attribute_bonus[bonus_property] += value
            else:
                self.attribute_bonus[bonus_property] = value

    def cal_avatar_eidolon_add(self):
        for attribute in self.avatar.eidolon_attribute:
            if attribute in self.attribute_bonus:
                self.attribute_bonus[
                    attribute
                ] += self.avatar.eidolon_attribute[attribute]
            else:
                self.attribute_bonus[
                    attribute
                ] = self.avatar.eidolon_attribute[attribute]
        for attribute in self.avatar.extra_ability_attribute:
            if attribute in self.attribute_bonus:
                self.attribute_bonus[
                    attribute
                ] += self.avatar.extra_ability_attribute[attribute]
            else:
                self.attribute_bonus[
                    attribute
                ] = self.avatar.extra_ability_attribute[attribute]

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

    async def cal_damage(self, skill_type):
        print(self.base_attr)
        print(self.attribute_bonus)
        # 检查武器战斗生效的buff
        logger.info('检查武器战斗生效的buff')
        self.attribute_bonus = await self.weapon.weapon_ability(
            self.base_attr, self.attribute_bonus
        )
        logger.info('检查遗器套装战斗生效的buff')
        for set_skill in self.relic_set.SetSkill:
            self.attribute_bonus = await set_skill.set_skill_ability(
                self.base_attr, self.attribute_bonus
            )
        merged_attr = await merge_attribute(
            self.base_attr, self.attribute_bonus
        )
        print(merged_attr)
        attack = merged_attr['attack']
        logger.info(f'攻击力: {attack}')
        # 模拟 同属性弱点 同等级 的怪物
        # 韧性条减伤
        enemy_damage_reduction = 0.1
        damage_reduction = 1 - enemy_damage_reduction
        logger.info(f'韧性区: {damage_reduction}')
        # 抗性区
        enemy_status_resistance = 0
        for attr in merged_attr:
            if attr.__contains__('ResistancePenetration'):
                # 先默认触发
                enemy_status_resistance = merged_attr[attr]
        resistance_area = 1 - (0 - enemy_status_resistance)
        logger.info(f'抗性区: {resistance_area}')

        # 防御区
        # 检查是否有 ignore_defence
        logger.info('检查是否有 ignore_defence')
        ignore_defence = 1
        for attr in merged_attr:
            if attr == 'ignore_defence':
                ignore_defence = 1 - merged_attr[attr]
                break
        logger.info(f'ignore_defence {ignore_defence}')
        enemy_defence = (self.avatar.avatar_level * 10 + 200) * ignore_defence
        defence_multiplier = (self.avatar.avatar_level * 10 + 200) / (
            self.avatar.avatar_level * 10 + 200 + enemy_defence
        )
        logger.info(f'防御区: {defence_multiplier}')

        # 技能区
        if skill_type == 'Normal':
            skill_multiplier = self.avatar.Normal()
        elif skill_type == 'BPSkill':
            skill_multiplier = self.avatar.BPSkill()
        elif skill_type == 'Ultra':
            skill_multiplier = self.avatar.Ultra()
        else:
            raise Exception('skill type error')
        logger.info(f'技能区: {skill_multiplier}')

        # 增伤区
        # TODO: 这里计算只考虑了希儿，需要重写 injury_area = self.avatar.Talent()
        injury_area = self.avatar.Talent()
        # 检查是否有对某一个技能的伤害加成
        logger.info('检查是否有对某一个技能的伤害加成')
        for attr in merged_attr:
            if attr.__contains__('DmgAdd'):
                attr_name = attr.split('DmgAdd')[0]
                if attr_name == skill_type:
                    logger.info(
                        f'{attr} 对 {skill_type} 有 {merged_attr[attr]} 伤害加成'
                    )
                    injury_area += merged_attr[attr]
        # 检查球有无符合属性的伤害加成
        logger.info('检查球有无符合属性的伤害加成')
        for attr in merged_attr:
            if attr.__contains__('AddedRatio'):
                attr_name = attr.split('AddedRatio')[0]
                if attr_name == self.avatar.avatar_element:
                    logger.info(
                        f'{attr} 对 {self.avatar.avatar_element} '
                        f'有 {merged_attr[attr]} 伤害加成'
                    )
                    injury_area += merged_attr[attr]
        logger.info(f'增伤区: {injury_area}')

        # 爆伤区
        critical_damage = merged_attr['CriticalDamage']
        # 检查是否有对特定技能的爆伤加成
        # Ultra_CriticalChance
        for attr in merged_attr:
            if attr.__contains__('_CriticalChance'):
                skill_name = attr.split('_')[0]
                if skill_name == skill_type:
                    logger.info(
                        f'{attr} 对 {skill_type} 有 {merged_attr[attr]} 爆伤加成'
                    )
                    critical_damage += merged_attr[attr]
        logger.info(f'暴伤: {critical_damage}')

        damage = (
            attack
            * skill_multiplier
            * injury_area
            * defence_multiplier
            * resistance_area
            * damage_reduction
            * critical_damage
        )
        logger.info(f'{skill_type} 伤害: {damage}')
