import json
from typing import List
from pathlib import Path

from .model import DamageInstanceSkill, DamageInstanceAvatar

path = Path(__file__).parent.parent
with Path.open(path / 'Excel' / 'SkillData.json', encoding='utf-8') as f:
    skill_dict = json.load(f)


class SingleSkill:
    def __init__(self, skill: DamageInstanceSkill):
        self.id = skill.skillId
        self.level = skill.skillLevel


class BaseSkills:
    Normal_: SingleSkill
    BPSkill_: SingleSkill
    Ultra_: SingleSkill
    Maze_: SingleSkill
    Talent_: SingleSkill

    @classmethod
    def create(
        cls, char: DamageInstanceAvatar, skills: List[DamageInstanceSkill]
    ):
        for skill in skills:
            skill_attack_type = skill.skillAttackType
            if skill_attack_type == 'Normal':
                cls.Normal_ = SingleSkill(skill)
            elif skill_attack_type == 'BPSkill':
                cls.BPSkill_ = SingleSkill(skill)
            elif skill_attack_type == 'Ultra':
                cls.Ultra_ = SingleSkill(skill)
            elif skill_attack_type == 'Maze':
                cls.Maze_ = SingleSkill(skill)
            elif skill_attack_type == '':
                cls.Talent_ = SingleSkill(skill)
            else:
                raise ValueError(
                    f'Unknown skillAttackType: {skill_attack_type}'
                )
        return cls
