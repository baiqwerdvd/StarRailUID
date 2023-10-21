import copy
from typing import Dict, List

from gsuid_core.logger import logger

from ..Role import calculate_damage
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

        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )

        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})

        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})

        # 计算大招伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})

        # 银狼降防终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        add_attr_bonus = copy.deepcopy(attribute_bonus)
        add_attr_bonus['ignore_defence'] = 0.45 + add_attr_bonus.get(
            'ignore_defence', 0
        )
        damagelist4 = await calculate_damage(
            base_attr,
            add_attr_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
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
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )

        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})

        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})

        # 计算大招伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})

        # 神君
        skill_multiplier = self.Skill_num('Talent', 'Talent')
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
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
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )

        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})

        # 计算战技伤害
        attnum = 3
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill') / attnum
        damagelist2 = await calculate_damage(
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
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})

        # 计算大招伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})

        if self.avatar_rank >= 1:
            skill_multiplier = self.Skill_num('Normal', 'Normal') * 0.5
            damagelist4 = await calculate_damage(
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
            damagelist4[2] += damage3
            skill_info_list.append({'name': '强化普攻', 'damagelist': damagelist4})

            skill_multiplier = (self.Skill_num('BPSkill', 'BPSkill') / 3) * 0.8
            damagelist5 = await calculate_damage(
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
            damagelist5[2] += damage3
            skill_info_list.append({'name': '强化战技', 'damagelist': damagelist5})

        logger.info(skill_info_list)
        return skill_info_list


class Danhengil(BaseAvatar):
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
        if self.avatar_rank >= 6:
            self.extra_ability_attribute[
                'Normal3_ImaginaryResistancePenetration'
            ] = 0.6

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('对拥有虚数属性弱点的敌方目标造成伤害时, 暴击伤害提高24%。')
        self.extra_ability_attribute['CriticalDamageBase'] = 0.24

    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        start_buff = 3
        add_buff = 1
        max_buff = 6
        if self.avatar_rank >= 1:
            start_buff = 6
            add_buff = 2
            max_buff = 10

        injury_add = self.Skill_num('Talent', 'Talent')
        critical_damage_add = self.Skill_num('BPSkill', 'BPSkill')
        critical_buff = 0
        if self.avatar_rank >= 4:
            critical_buff = critical_damage_add * 4

        skill_info_list = []
        # 计算普攻1伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal') / 2
        damage_c = 0
        damage_e = 0
        damage_a = 0
        add_attr_bonus: Dict[str, float] = {}
        for i in range(1, 3):
            add_attr_bonus = copy.deepcopy(attribute_bonus)
            damage_buff = min(max_buff, start_buff + (i - 1) * add_buff)
            add_attr_bonus[
                'AllDamageAddedRatio'
            ] = damage_buff * injury_add + add_attr_bonus.get(
                'AllDamageAddedRatio', 0
            )
            if self.avatar_rank >= 4:
                add_attr_bonus[
                    'CriticalDamageBase'
                ] = critical_buff + add_attr_bonus.get('CriticalDamageBase', 0)
            damage1, damage2, damage3 = await calculate_damage(
                base_attr,
                add_attr_bonus,
                'Normal',
                'Normal',
                self.avatar_element,
                skill_multiplier,
                self.avatar_level,
            )
            damage_c += damage1
            damage_e += damage2
            damage_a += damage3
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            add_attr_bonus,
            'Normal',
            'Normal',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        damage_a += damage3
        skill_info_list.append(
            {'name': '普攻', 'damagelist': [damage_c, damage_e, damage_a]}
        )

        # 计算瞬华伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal1') / 3
        damage_c = 0
        damage_e = 0
        damage_a = 0
        add_attr_bonus: Dict[str, float] = {}
        for i in range(1, 4):
            add_attr_bonus = copy.deepcopy(attribute_bonus)
            damage_buff = min(max_buff, start_buff + (i - 1) * add_buff)
            add_attr_bonus[
                'AllDamageAddedRatio'
            ] = damage_buff * injury_add + add_attr_bonus.get(
                'AllDamageAddedRatio', 0
            )
            if self.avatar_rank >= 4:
                add_attr_bonus[
                    'CriticalDamageBase'
                ] = critical_buff + add_attr_bonus.get('CriticalDamageBase', 0)
            damage1, damage2, damage3 = await calculate_damage(
                base_attr,
                add_attr_bonus,
                'Normal',
                'Normal1',
                self.avatar_element,
                skill_multiplier,
                self.avatar_level,
            )
            damage_c += damage1
            damage_e += damage2
            damage_a += damage3
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            add_attr_bonus,
            'Normal',
            'Normal',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        damage_a += damage3
        skill_info_list.append(
            {'name': '瞬华', 'damagelist': [damage_c, damage_e, damage_a]}
        )

        # 计算天矢阴伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal2') / 5
        damage_c = 0
        damage_e = 0
        damage_a = 0
        add_attr_bonus: Dict[str, float] = {}
        for i in range(1, 6):
            add_attr_bonus = copy.deepcopy(attribute_bonus)
            damage_buff = min(max_buff, start_buff + (i - 1) * add_buff)
            add_attr_bonus[
                'AllDamageAddedRatio'
            ] = damage_buff * injury_add + add_attr_bonus.get(
                'AllDamageAddedRatio', 0
            )
            if self.avatar_rank >= 4:
                add_attr_bonus[
                    'CriticalDamageBase'
                ] = critical_buff + add_attr_bonus.get('CriticalDamageBase', 0)
            elif i >= 4:
                critical_buff = (i - 3) * critical_damage_add
                add_attr_bonus[
                    'CriticalDamageBase'
                ] = critical_buff + add_attr_bonus.get('CriticalDamageBase', 0)
            damage1, damage2, damage3 = await calculate_damage(
                base_attr,
                add_attr_bonus,
                'Normal',
                'Normal2',
                self.avatar_element,
                skill_multiplier,
                self.avatar_level,
            )
            damage_c += damage1
            damage_e += damage2
            damage_a += damage3
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            add_attr_bonus,
            'Normal',
            'Normal',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        damage_a += damage3
        skill_info_list.append(
            {'name': '天矢阴', 'damagelist': [damage_c, damage_e, damage_a]}
        )

        # 计算盘拏耀跃伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal3') / 7
        damage_c = 0
        damage_e = 0
        damage_a = 0
        add_attr_bonus: Dict[str, float] = {}
        for i in range(1, 8):
            add_attr_bonus = copy.deepcopy(attribute_bonus)
            damage_buff = min(max_buff, start_buff + (i - 1) * add_buff)
            add_attr_bonus[
                'AllDamageAddedRatio'
            ] = damage_buff * injury_add + add_attr_bonus.get(
                'AllDamageAddedRatio', 0
            )
            if self.avatar_rank >= 4:
                add_attr_bonus[
                    'CriticalDamageBase'
                ] = critical_buff + add_attr_bonus.get('CriticalDamageBase', 0)
            elif i >= 4:
                critical_buff = (i - 3) * critical_damage_add
                add_attr_bonus[
                    'CriticalDamageBase'
                ] = critical_buff + add_attr_bonus.get('CriticalDamageBase', 0)
            damage1, damage2, damage3 = await calculate_damage(
                base_attr,
                add_attr_bonus,
                'Normal',
                'Normal3',
                self.avatar_element,
                skill_multiplier,
                self.avatar_level,
            )
            damage_c += damage1
            damage_e += damage2
            damage_a += damage3
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            add_attr_bonus,
            'Normal',
            'Normal',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        damage_a += damage3
        skill_info_list.append(
            {'name': '盘拏耀跃', 'damagelist': [damage_c, damage_e, damage_a]}
        )

        # 计算大招伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra') / 3
        damage_c = 0
        damage_e = 0
        damage_a = 0
        add_attr_bonus: Dict[str, float] = {}
        for _ in range(1, 4):
            add_attr_bonus = copy.deepcopy(attribute_bonus)
            damage_buff = min(max_buff, 10)
            add_attr_bonus[
                'AllDamageAddedRatio'
            ] = damage_buff * injury_add + add_attr_bonus.get(
                'AllDamageAddedRatio', 0
            )
            critical_buff = 4 * critical_damage_add
            add_attr_bonus[
                'CriticalDamageBase'
            ] = critical_buff + add_attr_bonus.get('CriticalDamageBase', 0)
            damage1, damage2, damage3 = await calculate_damage(
                base_attr,
                add_attr_bonus,
                'Ultra',
                'Ultra',
                self.avatar_element,
                skill_multiplier,
                self.avatar_level,
            )
            damage_c += damage1
            damage_e += damage2
            damage_a += damage3
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            add_attr_bonus,
            'Normal',
            'Normal',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        damage_a += damage3
        skill_info_list.append(
            {'name': '终结技', 'damagelist': [damage_c, damage_e, damage_a]}
        )
        logger.info(skill_info_list)
        return skill_info_list

class Argenti(BaseAvatar):
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
        if self.avatar_rank >= 1:
            self.eidolon_attribute['CriticalDamageBase'] = 0.4
        if self.avatar_rank >= 2:
            self.eidolon_attribute['AttackAddedRatio'] = 0.4
        if self.avatar_rank >= 6:
            self.eidolon_attribute['Ultra_PhysicalResistancePenetration'] = 0.3

    def extra_ability(self):
        self.extra_ability_attribute['AllDamageAddedRatio'] = 0.15
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        talent_cc_add = self.Skill_num('Talent', 'Talent')
        attribute_bonus['CriticalChanceBase'] = talent_cc_add * 10 + attribute_bonus.get('CriticalChanceBase', 0)
        if self.avatar_rank >= 4:
            attribute_bonus['CriticalDamageBase'] = 0.08 + attribute_bonus.get('CriticalDamageBase', 0)
            attribute_bonus['CriticalChanceBase'] = talent_cc_add * 2 + attribute_bonus.get('CriticalChanceBase', 0)
        
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})
        
        # 计算大招1伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技(90耗能)', 'damagelist': damagelist3})
        
        # 计算大招2伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra1')
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
        # 计算大招2额外伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra_add')
        damagelist5 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist5[0] = damagelist5[0] * 6 + damagelist4[0]
        damagelist5[1] = damagelist5[1] * 6 + damagelist4[1]
        damagelist5[2] = damagelist5[2] * 6 + damagelist4[2]
        skill_info_list.append({'name': '强化终结技(180耗能)', 'damagelist': damagelist5})
        return skill_info_list

class Clara(BaseAvatar):
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
            self.eidolon_attribute['AttackAddedRatio'] = 0.2

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('史瓦罗的反击造成的伤害提高30%')
        self.extra_ability_attribute['TalentDmgAdd'] = 0.3
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})
        
        # 计算反击伤害
        skill_multiplier = self.Skill_num('Talent', 'Talent')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '反击', 'damagelist': damagelist3})
        
        # 计算强化反击伤害
        skill_multiplier = self.Skill_num('Talent', 'Talent') + self.Skill_num('Ultra', 'Talent1')
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
        skill_info_list.append({'name': '强化反击', 'damagelist': damagelist4})
        
        return skill_info_list
    
class Silverwolf(BaseAvatar):
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
        if self.avatar_rank >= 6:
            self.extra_ability_attribute['AllDamageAddedRatio'] = 1

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('战技降抗')
        logger.info('战技使目标全属性抗性降低的效果额外降低3%')
        enemy_status_resistance = self.Skill_num('BPSkill', 'BPSkill_D') + 0.03
        self.extra_ability_attribute[
            'QuantumResistancePenetration'
        ] = enemy_status_resistance
        logger.info('终结技降防')
        ultra_defence = self.Skill_num('Ultra', 'Ultra_D')
        logger.info('天赋降防')
        talent_defence = self.Skill_num('Talent', 'Talent')
        ignore_defence = ultra_defence + talent_defence
        self.extra_ability_attribute['ignore_defence'] = ignore_defence
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        if self.avatar_rank >= 4:
            skill_multiplier += 1
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})
        
        return skill_info_list

class Kafka(BaseAvatar):
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
        if self.avatar_rank >= 1:
            self.extra_ability_attribute['DOTDmgAdd'] = 0.3
        if self.avatar_rank >= 2:
            self.extra_ability_attribute['DOTDmgAdd'] = 0.55

    def extra_ability(self):
        pass
        
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})
        
        # 计算持续伤害
        skill_multiplier = self.Skill_num('Ultra', 'DOT')
        if self.avatar_rank >= 6:
            skill_multiplier += 1.56
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'DOT',
            'DOT',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
        skill_info_list.append({'name': '单次持续伤害', 'damagelist': damagelist4})
        
        # 计算追加攻击伤害
        skill_multiplier = self.Skill_num('Talent', 'Talent')
        damagelist5 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist5[2] += damage3
        skill_info_list.append({'name': '追加攻击', 'damagelist': damagelist5})
        
        return skill_info_list

class Blade(BaseAvatar):
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
            self.eidolon_attribute['CriticalChanceBase'] = 0.15
        if self.avatar_rank >= 4:
            self.eidolon_attribute['HPAddedRatio'] = 0.4

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('天赋施放的追加攻击伤害提高20%')
        self.extra_ability_attribute['TalentDmgAdd'] = 0.2
        logger.info('战技加伤')
        self.extra_ability_attribute['AllDamageAddedRatio'] = self.Skill_num('BPSkill', 'BPSkill')
        
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算强化普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal1')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        
        skill_multiplier = self.Skill_num('Normal', 'Normal1_HP')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
            1,
        )
        damagelist3[0] += damagelist2[0]
        damagelist3[1] += damagelist2[1]
        damagelist3[2] += damagelist2[2]
        skill_info_list.append({'name': '无间剑树', 'damagelist': damagelist3})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
        
        skill_multiplier = self.Skill_num('Ultra', 'Ultra_HP')
        if self.avatar_rank >= 1:
            skill_multiplier += 0.9
        damagelist5 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
            1,
        )
        damagelist5[0] += damagelist4[0]
        damagelist5[1] += damagelist4[1]
        damagelist5[2] += damagelist4[2]
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist5})
        
        # 计算追加攻击伤害
        skill_multiplier = self.Skill_num('Talent', 'Talent')
        damagelist6 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist6[2] += damage3
        
        skill_multiplier = self.Skill_num('Talent', 'Talent_HP')
        damagelist7 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
            1,
        )
        damagelist7[0] += damagelist6[0]
        damagelist7[1] += damagelist6[1]
        damagelist7[2] += damagelist6[2]
        if self.avatar_rank >= 6:
            hp = base_attr['hp'] * (1 + attribute_bonus['HPAddedRatio']) + attribute_bonus['HPDelta']
            damage_add = hp * 0.5
            damagelist7[0] += damage_add
            damagelist7[1] += damage_add
            damagelist7[2] += damage_add
        skill_info_list.append({'name': '追加攻击', 'damagelist': damagelist7})
        
        return skill_info_list

class Fuxuan(BaseAvatar):
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
        if self.avatar_rank >= 1:
            self.eidolon_attribute['CriticalDamageBase'] = 0.3

    def extra_ability(self):
        logger.info('符玄战技【穷观阵】属性加成')
        self.extra_ability_attribute['CriticalChanceBase'] = self.Skill_num('BPSkill', 'BPSkill_CC')
        self.extra_ability_attribute['HPAddedRatio'] = self.Skill_num('BPSkill', 'BPSkill_HP')
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal_HP')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
            1,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra_HP')
        if self.avatar_rank >= 6:
            skill_multiplier += 1.2
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
            1,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist2})
        
        return skill_info_list

class Yanqing(BaseAvatar):
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
        if self.avatar_rank >= 4:
            self.eidolon_attribute['IceResistancePenetration'] = 0.15

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('触发暴击时, 速度提高10%')
        self.extra_ability_attribute['SpeedAddedRatio'] = 0.1
        logger.info('【智剑连心】增益')
        critical_damage_base_t = self.Skill_num('Talent', 'Talent_CD')
        critical_damage_base_u = self.Skill_num('Ultra', 'Ultra_CD')
        self.extra_ability_attribute['CriticalDamageBase'] = (
            critical_damage_base_t + critical_damage_base_u
        )
        critical_chance_base = self.Skill_num('Talent', 'Talent_CC')
        self.extra_ability_attribute['CriticalChanceBase'] = (
            critical_chance_base + 0.6
        )
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})
        
        # 计算附加伤害
        skill_multiplier = self.Skill_num('Talent', 'Talent')
        if self.avatar_rank >= 1:
            skill_multiplier += 0.9
        else:
            skill_multiplier += 0.3
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
        skill_info_list.append({'name': '附加伤害', 'damagelist': damagelist4})
        
        return skill_info_list

class Himeko(BaseAvatar):
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
        if self.avatar_rank >= 1:
            self.eidolon_attribute['SpeedAddedRatio'] = 0.1
        if self.avatar_rank >= 2:
            self.eidolon_attribute['AllDamageAddedRatio'] = 0.15

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('战技对灼烧状态下的敌方目标造成的伤害提高20%。')
        self.extra_ability_attribute['BPSkillDmgAdd'] = 0.2
        logger.info('若当前生命值百分比大于等于80%, 则暴击率提高15%。')
        self.extra_ability_attribute['CriticalChanceBase'] = 0.15
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})
        
        # 计算追加攻击伤害
        skill_multiplier = self.Skill_num('Talent', 'Talent')
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
        skill_info_list.append({'name': '追加攻击', 'damagelist': damagelist4})
        
        return skill_info_list

class Qingque(BaseAvatar):
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
        if self.avatar_rank >= 1:
            self.eidolon_attribute['UltraDmgAdd'] = 0.1

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('施放强化普攻后, 青雀的速度提高10%, 持续1回合。')
        self.extra_ability_attribute['SpeedAddedRatio'] = 0.1
        logger.info('默认4层战技加伤害')
        all_damage_added_ratio = self.Skill_num('BPSkill', 'BPSkill') + 0.1
        self.extra_ability_attribute['AllDamageAddedRatio'] = (
            all_damage_added_ratio * 4
        )
        logger.info('默认暗杠加攻')
        self.extra_ability_attribute['AttackAddedRatio'] = self.Skill_num('Talent', 'Talent')
        
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算杠上开花伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal1')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '杠上开花！', 'damagelist': damagelist2})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})
        
        return skill_info_list

class Jingliu(BaseAvatar):
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
        if self.avatar_rank >= 1:
            self.eidolon_attribute['CriticalDamageBase'] = 0.24
        if self.avatar_rank >= 2:
            self.eidolon_attribute['BPSkill1DmgAdd'] = 0.8
        if self.avatar_rank >= 4:
            self.eidolon_attribute['BPSkill1AttackAddedRatio'] = 0.3
            self.eidolon_attribute['UltraAttackAddedRatio'] = 0.3
        if self.avatar_rank >= 6:
            self.eidolon_attribute['Ultra_CriticalDamageBase'] = 0.5
            self.eidolon_attribute['BPSkill1_CriticalDamageBase'] = 0.5

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('【转魄】状态下, 终结技造成的伤害提高20%。')
        logger.info('【转魄】状态下, 暴击率提高。')
        logger.info('【转魄】状态下, 攻击力提高。')
        self.extra_ability_attribute['UltraDmgAdd'] = 0.2
        critical_chance_base = self.Skill_num('Talent', 'Talent_CC')
        self.extra_ability_attribute[
            'Ultra_CriticalChanceBase'
        ] = critical_chance_base
        self.extra_ability_attribute[
            'BPSkill1_CriticalChanceBase'
        ] = critical_chance_base
        attack_added_ratio = self.Skill_num('Talent', 'Talent_atk')
        self.extra_ability_attribute[
            'BPSkill1AttackAddedRatio'
        ] = attack_added_ratio
        self.extra_ability_attribute[
            'UltraAttackAddedRatio'
        ] = attack_added_ratio
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})
        
        # 计算寒川映月伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill1')
        if self.avatar_rank >= 1:
            skill_multiplier += 1
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill1',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '寒川映月', 'damagelist': damagelist3})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        if self.avatar_rank >= 1:
            skill_multiplier += 1
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist4})
        
        return skill_info_list

class Topaz(BaseAvatar):
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
        if self.avatar_rank >= 1:
            self.eidolon_attribute['Talent_CriticalDamageBase'] = 0.5
        if self.avatar_rank >= 6:
            self.eidolon_attribute['Talent1_FireResistancePenetration'] = 0.1

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('托帕和账账对拥有火属性弱点的敌方目标造成的伤害提高15%。')
        self.extra_ability_attribute['AllDamageAddedRatio'] = 0.15
        logger.info('涨幅惊人暴击伤害提高')
        self.extra_ability_attribute[
            'Talent1_CriticalDamageBase'
        ] = self.Skill_num('Ultra', 'Ultra_CD')
        logger.info('【负债证明】状态,使其受到的追加攻击伤害提高')
        self.extra_ability_attribute['TalentDmgAdd'] = self.Skill_num(
            'BPSkill', 'BPSkill_add'
        )
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算账账伤害
        skill_multiplier = self.Skill_num('Talent', 'Talent')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '账账', 'damagelist': damagelist2})
        
        # 计算强化账账伤害
        skill_multiplier = self.Skill_num('Talent', 'Talent') + self.Skill_num('Ultra', 'Talent1')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Talent',
            'Talent1',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '强化账账', 'damagelist': damagelist3})
        
        return skill_info_list

class Guinaifen(BaseAvatar):
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
        self.extra_ability_attribute['AllDamageAddedRatio'] = 0.2
        if self.avatar_rank >= 6:
            self.extra_ability_attribute['DmgRatio'] = (
                self.Skill_num('Talent', 'Talent') * 4
            )
        else:
            self.extra_ability_attribute['DmgRatio'] = (
                self.Skill_num('Talent', 'Talent') * 3
            )
    
    async def getdamage(
        self,
        base_attr: Dict[str, float],
        attribute_bonus: Dict[str, float],
    ):
        damage1, damage2, damage3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'fujia',
            'fujia',
            'Thunder',
            0.44,
            self.avatar_level,
        )
        
        skill_info_list = []
        # 计算普攻伤害
        skill_multiplier = self.Skill_num('Normal', 'Normal')
        damagelist1 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Normal',
            'Normal',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist1[2] += damage3
        skill_info_list.append({'name': '普攻', 'damagelist': damagelist1})
        
        # 计算战技伤害
        skill_multiplier = self.Skill_num('BPSkill', 'BPSkill')
        damagelist2 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'BPSkill',
            'BPSkill',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist2[2] += damage3
        skill_info_list.append({'name': '战技', 'damagelist': damagelist2})
        
        # 计算终结技伤害
        skill_multiplier = self.Skill_num('Ultra', 'Ultra')
        damagelist3 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'Ultra',
            'Ultra',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist3[2] += damage3
        skill_info_list.append({'name': '终结技', 'damagelist': damagelist3})
        
        # 计算持续伤害
        skill_multiplier = self.Skill_num('BPSkill', 'DOT')
        if self.avatar_rank >= 2:
            skill_multiplier += 0.4
        damagelist4 = await calculate_damage(
            base_attr,
            attribute_bonus,
            'DOT',
            'DOT',
            self.avatar_element,
            skill_multiplier,
            self.avatar_level,
        )
        damagelist4[2] += damage3
        skill_info_list.append({'name': '单次持续伤害', 'damagelist': damagelist4})
        
        return skill_info_list
    
class AvatarDamage:
    @classmethod
    def create(
        cls, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        if char.id_ == 1210:
            return Guinaifen(char, skills)
        if char.id_ == 1302:
            return Argenti(char, skills)
        if char.id_ == 1112:
            return Topaz(char, skills)
        if char.id_ == 1005:
            return Kafka(char, skills)
        if char.id_ == 1201:
            return Qingque(char, skills)
        if char.id_ == 1212:
            return Jingliu(char, skills)
        if char.id_ == 1107:
            return Clara(char, skills)
        if char.id_ == 1205:
            return Blade(char, skills)
        if char.id_ == 1003:
            return Himeko(char, skills)
        if char.id_ == 1209:
            return Yanqing(char, skills)
        if char.id_ == 1102:
            return Seele(char, skills)
        if char.id_ == 1208:
            return Fuxuan(char, skills)
        if char.id_ == 1006:
            return Silverwolf(char, skills)
        if char.id_ == 1204:
            return JingYuan(char, skills)
        if char.id_ == 1004:
            return Welt(char, skills)
        if char.id_ == 1213:
            return Danhengil(char, skills)
        raise Exception('不支持的角色')
