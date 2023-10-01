from typing import Dict, List

from gsuid_core.logger import logger

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
        self.extra_ability_attribute['UltraDmgAdd'] = 0.3


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
        if self.avatar_rank >= 1:
            self.eidolon_attribute['Atk_buff'] = 1
        if self.avatar_rank >= 4:
            self.eidolon_attribute['Normal_buff'] = 4
        if self.avatar_rank >= 6:
            self.extra_ability_attribute[
                'Normal3_ImaginaryResistancePenetration'
            ] = 0.6

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('对拥有虚数属性弱点的敌方目标造成伤害时, 暴击伤害提高24%。')
        self.extra_ability_attribute['CriticalDamageBase'] = 0.24


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
        enemy_status_resistance = self.BPSkill_num('BPSkill_D') + 0.03
        self.extra_ability_attribute[
            'QuantumResistancePenetration'
        ] = enemy_status_resistance
        logger.info('终结技降防')
        ultra_defence = self.Ultra_num('Ultra_D')
        logger.info('天赋降防')
        talent_defence = self.Talent()
        ignore_defence = ultra_defence + talent_defence
        self.extra_ability_attribute['ignore_defence'] = ignore_defence


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
        self.extra_ability_attribute['CriticalChanceBase'] = self.BPSkill_num(
            'BPSkill_CC'
        )
        self.extra_ability_attribute['HPAddedRatio'] = self.BPSkill_num(
            'BPSkill_HP'
        )


class Gepard(BaseAvatar):
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
        pass


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
        critical_damage_base_t = self.Talent_num('Talent_CD')
        critical_damage_base_u = self.Ultra_num('Ultra_CD')
        self.extra_ability_attribute['CriticalDamageBase'] = (
            critical_damage_base_t + critical_damage_base_u
        )
        critical_chance_base = self.Talent_num('Talent_CC')
        self.extra_ability_attribute['CriticalChanceBase'] = (
            critical_chance_base + 0.6
        )


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
        logger.info('对被弱点击破的敌方目标造成的伤害提高20')
        self.extra_ability_attribute['AllDamageAddedRatio'] = 0.32


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
        all_damage_added_ratio = self.BPSkill() + 0.1
        self.extra_ability_attribute['AllDamageAddedRatio'] = (
            all_damage_added_ratio * 4
        )
        logger.info('默认暗杠加攻')
        self.extra_ability_attribute['AttackAddedRatio'] = self.Talent()


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
        critical_chance_base = self.Talent_num('Talent_CC')
        self.extra_ability_attribute[
            'Ultra_CriticalChanceBase'
        ] = critical_chance_base
        self.extra_ability_attribute[
            'BPSkill1_CriticalChanceBase'
        ] = critical_chance_base
        attack_added_ratio = self.Talent_num('Talent_atk')
        self.extra_ability_attribute[
            'BPSkill1AttackAddedRatio'
        ] = attack_added_ratio
        self.extra_ability_attribute[
            'UltraAttackAddedRatio'
        ] = attack_added_ratio


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
        ] = self.Ultra_num('Ultra_CD')
        logger.info('【负债证明】状态,使其受到的追加攻击伤害提高')
        self.extra_ability_attribute['TalentDmgAdd'] = self.BPSkill_num(
            'BPSkill_add'
        )


class Avatar:
    @classmethod
    def create(
        cls, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        if char.id_ == 1112:
            return Topaz(char, skills)
        if char.id_ == 1212:
            return Jingliu(char, skills)
        if char.id_ == 1201:
            return Qingque(char, skills)
        if char.id_ == 1003:
            return Himeko(char, skills)
        if char.id_ == 1004:
            return Welt(char, skills)
        if char.id_ == 1209:
            return Yanqing(char, skills)
        if char.id_ == 1104:
            return Gepard(char, skills)
        if char.id_ == 1208:
            return Fuxuan(char, skills)
        if char.id_ == 1205:
            return Blade(char, skills)
        if char.id_ == 1005:
            return Kafka(char, skills)
        if char.id_ == 1006:
            return Silverwolf(char, skills)
        if char.id_ == 1213:
            return Danhengil(char, skills)
        if char.id_ == 1102:
            return Seele(char, skills)
        if char.id_ == 1204:
            return JingYuan(char, skills)
        if char.id_ == 1107:
            return Clara(char, skills)
        raise Exception('不支持的角色')
