from typing import List

from mpmath import mp
from gsuid_core.logger import logger

from ..Base.AvatarBase import BaseAvatar, BaseAvatarBuff
from ..Base.model import DamageInstanceSkill, DamageInstanceAvatar

mp.dps = 14


class Seele(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank < 2:
            self.eidolon_attribute['SpeedAddedRatio'] = mp.mpf(0.25)
        if self.avatar_rank >= 1:
            self.eidolon_attribute['CriticalChanceBase'] = mp.mpf(0.15)
        if self.avatar_rank >= 2:
            self.eidolon_attribute['SpeedAddedRatio'] = mp.mpf(0.5)

    def extra_ability(self):
        # 额外能力 割裂 抗性穿透提高20
        self.extra_ability_attribute['QuantumResistancePenetration'] = mp.mpf(
            0.2
        )


class JingYuan(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 2:
            self.eidolon_attribute['NormalDmgAdd'] = mp.mpf(0.2)
            self.eidolon_attribute['BPSkillDmgAdd'] = mp.mpf(0.2)
            self.eidolon_attribute['UltraDmgAdd'] = mp.mpf(0.2)
        if self.avatar_rank >= 6:
            self.eidolon_attribute['Talent_DmgRatio'] = mp.mpf(0.288)

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('【神君】下回合的攻击段数大于等于6段，则其下回合的暴击伤害提高25%。')
        self.extra_ability_attribute['CriticalDamageBase'] = mp.mpf(0.25)
        logger.info('施放战技后，暴击率提升10%')
        self.extra_ability_attribute['CriticalChanceBase'] = mp.mpf(0.1)


class Clara(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 2:
            self.eidolon_attribute['AttackAddedRatio'] = mp.mpf(0.2)

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('史瓦罗的反击造成的伤害提高30%')
        self.extra_ability_attribute['TalentDmgAdd'] = mp.mpf(0.3)
        self.extra_ability_attribute['UltraDmgAdd'] = mp.mpf(0.3)


class Danhengil(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 1:
            self.eidolon_attribute['Atk_buff'] = mp.mpf(1)
        if self.avatar_rank >= 4:
            self.eidolon_attribute['Normal_buff'] = mp.mpf(4)
        if self.avatar_rank >= 6:
            self.extra_ability_attribute[
                'Normal_ImaginaryResistancePenetration'
            ] = mp.mpf(0.6)

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('对拥有虚数属性弱点的敌方目标造成伤害时，暴击伤害提高24%。')
        self.extra_ability_attribute['CriticalDamageBase'] = mp.mpf(0.24)


class Silverwolf(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 6:
            self.extra_ability_attribute['AllDamageAddedRatio'] = mp.mpf(1)

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('战技降抗')
        logger.info('战技使目标全属性抗性降低的效果额外降低3%')
        enemy_status_resistance = self.BPSkill_num('BPSkill_D') + 0.03
        self.extra_ability_attribute['QuantumResistancePenetration'] = mp.mpf(
            enemy_status_resistance
        )
        logger.info('终结技降防')
        ultra_defence = self.Ultra_num('Ultra_D')
        logger.info('天赋降防')
        talent_defence = self.Talent()
        ignore_defence = ultra_defence + talent_defence
        self.extra_ability_attribute['ignore_defence'] = mp.mpf(ignore_defence)


class Kafka(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 1:
            self.extra_ability_attribute['DOTDmgAdd'] = mp.mpf(0.3)
        if self.avatar_rank >= 2:
            self.extra_ability_attribute['DOTDmgAdd'] = mp.mpf(0.55)

    def extra_ability(self):
        pass


class Blade(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 2:
            self.eidolon_attribute['CriticalChanceBase'] = mp.mpf(0.15)

        if self.avatar_rank >= 4:
            self.extra_ability_attribute['HPAddedRatio'] = mp.mpf(0.4)

    def extra_ability(self):
        logger.info('额外能力')
        logger.info('天赋施放的追加攻击伤害提高20%')
        self.extra_ability_attribute['TalentDmgAdd'] = mp.mpf(0.2)


class Fuxuan(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 1:
            self.eidolon_attribute['CriticalDamageBase'] = mp.mpf(0.3)

    def extra_ability(self):
        pass


class Gepard(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(
        self, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        super().__init__(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        pass

    def extra_ability(self):
        pass


class Avatar:
    @classmethod
    def create(
        cls, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
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
