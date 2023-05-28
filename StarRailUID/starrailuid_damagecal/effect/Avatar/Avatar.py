from typing import Dict, List

from mpmath import mp

from ..Base.AvatarBase import BaseAvatar, BaseAvatarBuff

mp.dps = 14


class Seele(BaseAvatar):
    Buff: BaseAvatarBuff

    def __init__(self, char: Dict, skills: List):
        super().__init__(char=char, skills=skills)
        self.Buff = BaseAvatarBuff(char=char, skills=skills)
        self.eidolon_attribute = {}
        self.extra_ability_attribute = {}
        self.eidolons()
        self.extra_ability()

    def Technique(self):
        pass

    def eidolons(self):
        if self.avatar_rank >= 1:
            self.eidolon_attribute['CriticalDamageBase'] = mp.mpf(0.15)
        if self.avatar_rank >= 2:
            self.eidolon_attribute['SpeedAddedRatio'] = mp.mpf(0.5)

    def extra_ability(self):
        # 额外能力 割裂 抗性穿透提高20
        if 1102102 in self.Buff.extra_ability_id:
            self.extra_ability_attribute[
                'QuantumResistancePenetration'
            ] = mp.mpf(0.2)


class Avatar:
    def __new__(cls, char: Dict, skills: List):
        if char['id'] == 1102:
            return Seele(char, skills)
