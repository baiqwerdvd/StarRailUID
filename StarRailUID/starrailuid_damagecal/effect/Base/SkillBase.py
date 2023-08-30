import json
from pathlib import Path
from typing import Dict, List

from mpmath import mp

mp.dps = 14


path = Path(__file__).parent.parent
with Path.open(path / 'Excel' / 'seele.json', encoding='utf-8') as f:
    skill_dict = json.load(f)


class SingleSkill:
    def __init__(self, skill: Dict):
        self.id = skill['skillId']
        self.level = skill['skillLevel']


class BaseSkills:
    Normal_: SingleSkill
    BPSkill_: SingleSkill
    Ultra_: SingleSkill
    Maze_: SingleSkill
    Talent_: SingleSkill

    def __init__(self, char: Dict, skills: List):
        for skill in skills:
            skill_attack_type = skill['skillAttackType']
            if skill_attack_type == 'Normal':
                self.Normal_ = SingleSkill(skill)
            elif skill_attack_type == 'BPSkill':
                self.BPSkill_ = SingleSkill(skill)
            elif skill_attack_type == 'Ultra':
                self.Ultra_ = SingleSkill(skill)
            elif skill_attack_type == 'Maze':
                self.Maze_ = SingleSkill(skill)
            elif skill_attack_type == '':
                self.Talent_ = SingleSkill(skill)
            else:
                raise ValueError(
                    f'Unknown skillAttackType: {skill_attack_type}'
                )
