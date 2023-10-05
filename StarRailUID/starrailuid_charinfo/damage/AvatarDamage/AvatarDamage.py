import copy
from typing import Dict, List

from gsuid_core.logger import logger

from ..Role import demage_num
from ..Base.AvatarBase import BaseAvatar, BaseAvatarBuff
from ..Base.model import DamageInstanceSkill, DamageInstanceAvatar


class Seele(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute: Dict[str, float] = {}
        self.extra_ability_attribute: Dict[str, float] = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank < 2:
            self.eidolon_attribute['SpeedAddedRatio'] = 0.25
        if self.avatar_rank >= 1:
            self.eidolon_attribute['CriticalChanceBase'] = 0.15
        if self.avatar_rank >= 2:
            self.eidolon_attribute['SpeedAddedRatio'] = 0.5

    def extra_ability(self):
        # 额外能力 割裂 抗性穿透提高20
        self.extra_ability_attribute['QuantumResistancePenetration'] = 0.2

    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        # logger.info(base_attr)
        # logger.info(self.avatar_rank)

        # 希尔天赋再现加伤害
        attribute_bonus['AllDamageAddedRatio'] = self.Skill_num(
            'Talent', 'Talent'
        ) + attribute_bonus.get('AllDamageAddedRatio', 0)

        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await demage_num(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})

        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await demage_num(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})

        # 计算大招伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await demage_num(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})

        # 银狼降防终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        add_attr_bonus = copy.deepcopy(attribute_bonus)
        add_attr_bonus['ignore_defence'] = 0.45 + add_attr_bonus.get(
            'ignore_defence', 0
        )
        damagelist4 = await demage_num(
            base_attr,
            add_attr_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '银狼降防终结技', 'damagelist': damagelist4})

        logger.info(skill_info_list)
        return skill_info_list


class JingYuan(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute: Dict[str, float] = {}
        self.extra_ability_attribute: Dict[str, float] = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 2:
            self.eidolon_attribute['NormalDmgAdd'] = 0.2
            self.eidolon_attribute['BPSkillDmgAdd'] = 0.2
            self.eidolon_attribute['UltraDmgAdd'] = 0.2
        if self.avatar_rank >= 6:
            self.eidolon_attribute['Talent_DmgRatio'] = 0.288

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('【神君】下回合的攻击段数大于等于6段, 则其下回合的暴击伤害提高25%。')
        self.extra_ability_attribute['CriticalDamageBase'] = 0.25
        logger.info('施放战技后, 暴击率提升10%')
        self.extra_ability_attribute['CriticalChanceBase'] = 0.1

    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await demage_num(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})

        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await demage_num(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})

        # 计算大招伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await demage_num(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})

        # 神君
        skill_multiplier = self.Skill_num('Talent', 'Talent')
        damagelist4 = await demage_num(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '10层神君伤害', 'damagelist': damagelist4})

        logger.info(skill_info_list)
        return skill_info_list


class Welt(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute: Dict[str, float] = {}
        self.extra_ability_attribute: Dict[str, float] = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        pass

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('施放终结技时, 有100%基础概率使目标受到的伤害提高12%, 持续2回合。')
        self.extra_ability_attribute['DmgRatio'] = 0.12
        logger.info('对被弱点击破的敌方目标造成的伤害提高20')
        self.extra_ability_attribute['AllDamageAddedRatio'] = 0.20

    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await demage_num(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})

        # 计算战技伤害
        attnum = 3
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill') / attnum
        damagelist2 = await demage_num(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        if self.avatar_rank >= 6:
            attnum = 4
        damagelist2[0] = damagelist2[0] * attnum
        damagelist2[1] = damagelist2[1] * attnum
        damagelist2[2] = damagelist2[2] * attnum
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})

        # 计算大招伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await demage_num(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})

        if self.avatar_rank >= 1:
            skill_multiplier = self.Skill_num('Normal', 'Normal') * 0.5
            damagelist4 = await demage_num(
                base_attr,
                attribute_bonus,
                'Normal',
                'Normal',
                self.avatar_element,
                skill_multiplier,
                self.avatar_level,
            )
            damagelist4[0] = damagelist1[0] + damagelist4[0]
            damagelist4[1] = damagelist1[1] + damagelist4[1]
            damagelist4[2] = damagelist1[2] + damagelist4[2]
            skill_info_list.append({'name': '强化普攻', 'damagelist': damagelist4})

            skill_multiplier = (self.Skill_num('BPSkill', 'BPSkill') / 3) * 0.8
            damagelist5 = await demage_num(
                base_attr,
                attribute_bonus,
                'BPSkill',
                'BPSkill',
                self.avatar_element,
                skill_multiplier,
                self.avatar_level,
            )
            damagelist5[0] = damagelist2[0] + damagelist5[0]
            damagelist5[1] = damagelist2[1] + damagelist5[1]
            damagelist5[2] = damagelist2[2] + damagelist5[2]
            skill_info_list.append({'name': '强化战技', 'damagelist': damagelist5})

        logger.info(skill_info_list)
        return skill_info_list


class AvatarDamage:
    @classmethod
    def create(
        cls, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        if char.id_ == 1102:
            return Seele(char, skills)
        if char.id_ == 1204:
            return JingYuan(char, skills)
        if char.id_ == 1004:
            return Welt(char, skills)
        raise Exception('不支持的角色')
