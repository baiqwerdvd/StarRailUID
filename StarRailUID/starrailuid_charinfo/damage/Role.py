from typing import Dict

from gsuid_core.logger import logger

from .utils import merge_attribute


async def calculate_damage(
    base_attr: Dict[str, float],
    attribute_bonus: Dict[str, float],
    skill_type: str,
    add_skill_type: str,
    element: str,
    skill_multiplier: float,
    level: int,
):
    logger.info(f'Skill Multiplier: {skill_multiplier}')
    logger.info(f'Skill Type: {skill_type}')
    logger.info(f'Level: {level}')
    # logger.info(f'attribute_bonus: {attribute_bonus}')

    attribute_bonus = apply_attribute_bonus(
        attribute_bonus, skill_type, add_skill_type
    )

    merged_attr = await merge_attribute(base_attr, attribute_bonus)
    # logger.info(f'merged_attr: {merged_attr}')

    attack = merged_attr.get('attack', 0)
    logger.info(f'Attack: {attack}')

    damage_reduction = calculate_damage_reduction(level)
    logger.info(f'韧性区: {damage_reduction}')

    resistance_area = calculate_resistance_area(
        merged_attr, skill_type, add_skill_type, element
    )
    logger.info(f'抗性区: {resistance_area}')

    defence_multiplier = calculate_defence_multiplier(level, merged_attr)
    logger.info(f'防御区: {defence_multiplier}')

    injury_area, element_area = calculate_injury_area(
        merged_attr, skill_type, add_skill_type, element
    )
    logger.info(f'增伤区: {injury_area}')

    damage_ratio = calculate_damage_ratio(
        merged_attr, skill_type, add_skill_type
    )
    logger.info(f'易伤区: {damage_ratio}')

    critical_damage = calculate_critical_damage(
        merged_attr, skill_type, add_skill_type
    )
    logger.info(f'爆伤区: {critical_damage}')

    critical_chance = calculate_critical_chance(
        merged_attr, skill_type, add_skill_type
    )
    logger.info(f'暴击区: {critical_chance}')

    expected_damage = calculate_expected_damage(
        critical_chance, critical_damage
    )
    logger.info(f'暴击期望: {expected_damage}')

    damage_cd = calculate_damage_cd(
        attack,
        skill_multiplier,
        damage_ratio,
        injury_area,
        defence_multiplier,
        resistance_area,
        damage_reduction,
        critical_damage,
    )
    damage_qw = calculate_damage_qw(
        attack,
        skill_multiplier,
        damage_ratio,
        injury_area,
        defence_multiplier,
        resistance_area,
        damage_reduction,
        expected_damage,
    )

    damage_tz = calculate_damage_tz(
        attack,
        skill_multiplier,
        damage_ratio,
        injury_area,
        defence_multiplier,
        resistance_area,
        damage_reduction,
        critical_damage,
        element,
        element_area,
        base_attr,
    )

    skill_info_list = [damage_cd, damage_qw, damage_tz]

    logger.info(
        f'Critical Damage: {damage_cd} Expected Damage: {damage_qw} Apocalypse Damage: {damage_tz}'
    )

    return skill_info_list


def apply_attribute_bonus(
    attribute_bonus: Dict[str, float],
    skill_type: str,
    add_skill_type: str,
):
    # Apply attribute bonuses to attack and status probability
    for attr in attribute_bonus:
        if 'AttackAddedRatio' in attr and attr.split('AttackAddedRatio')[
            0
        ] in (skill_type, add_skill_type):
            attribute_bonus['AttackAddedRatio'] += attribute_bonus[attr]
        if 'StatusProbabilityBase' in attr and attr.split(
            'StatusProbabilityBase'
        )[0] in (skill_type, add_skill_type):
            attribute_bonus['StatusProbabilityBase'] += attribute_bonus[attr]
    return attribute_bonus


def calculate_damage_reduction(level: int):
    enemy_damage_reduction = 0.1
    return 1 - enemy_damage_reduction


def calculate_resistance_area(
    merged_attr: Dict[str, float],
    skill_type: str,
    add_skill_type: str,
    element: str,
):
    enemy_status_resistance = 0.0
    for attr in merged_attr:
        if 'ResistancePenetration' in attr:
            # 检查是否有某一属性的抗性穿透
            attr_name = attr.split('ResistancePenetration')[0]
            if attr_name in (element, 'AllDamage'):
                # logger.info(f'{attr_name}属性有{merged_attr[attr]}穿透加成')
                enemy_status_resistance += merged_attr[attr]
            # 检查是否有某一技能属性的抗性穿透
            if '_' in attr_name:
                skill_name = attr_name.split('_')[0]
                skillattr_name = attr_name.split('_')[1]
                if skill_name == add_skill_type and skillattr_name in (
                    element,
                    'AllDamage',
                ):
                    enemy_status_resistance += merged_attr[attr]
                    # logger.info(
                    # f'{skill_name}对{skillattr_name}属性有{merged_attr[attr]}穿透加成'
                    # )
    return 1.0 - (0 - enemy_status_resistance)


def calculate_defence_multiplier(
    level: int,
    merged_attr: Dict[str, float],
):
    ignore_defence = merged_attr.get('ignore_defence', 0.0)
    enemy_defence = (level * 10 + 200) * (1 - ignore_defence)
    return (level * 10 + 200) / (level * 10 + 200 + enemy_defence)


def calculate_injury_area(
    merged_attr: Dict[str, float],
    skill_type: str,
    add_skill_type: str,
    element: str,
):
    injury_area = 0.0
    element_area = 0.0
    for attr in merged_attr:
        attr_name = attr.split('AddedRatio')[0]
        skill_name = attr.split('DmgAdd')[0]
        if 'DmgAdd' in attr and skill_name in (
            skill_type,
            add_skill_type,
        ):
            # logger.info(
            # f'{attr} 对 {skill_type} 有 {merged_attr[attr]} 伤害加成'
            # )
            injury_area += merged_attr[attr]

        if 'AddedRatio' in attr and attr_name in (
            element,
            'AllDamage',
        ):
            # logger.info(
            # f'{attr} 对 {element} 属性有 {merged_attr[attr]} 伤害加成'
            # )
            if attr_name == element:
                element_area += merged_attr[attr]
            injury_area += merged_attr[attr]
    return injury_area + 1, element_area


def calculate_damage_ratio(
    merged_attr: Dict[str, float],
    skill_type: str,
    add_skill_type: str,
):
    damage_ratio = merged_attr.get('DmgRatio', 0)
    for attr in merged_attr:
        if '_DmgRatio' in attr and attr.split('_')[0] in (
            skill_type,
            add_skill_type,
        ):
            damage_ratio += merged_attr[attr]
    return damage_ratio + 1


def calculate_critical_damage(
    merged_attr: Dict[str, float],
    skill_type: str,
    add_skill_type: str,
):
    if skill_type == 'DOT':
        return 1.0
    critical_damage_base = merged_attr.get('CriticalDamageBase', 0)
    for attr in merged_attr:
        if '_CriticalDamageBase' in attr and attr.split('_')[0] in (
            skill_type,
            add_skill_type,
        ):
            critical_damage_base += merged_attr[attr]
    return critical_damage_base + 1


def calculate_critical_chance(
    merged_attr: Dict[str, float],
    skill_type: str,
    add_skill_type: str,
):
    critical_chance_base = merged_attr['CriticalChanceBase']
    for attr in merged_attr:
        if '_CriticalChance' in attr and attr.split('_')[0] in (
            skill_type,
            add_skill_type,
        ):
            critical_chance_base += merged_attr[attr]
    return min(1, critical_chance_base)


def calculate_expected_damage(
    critical_chance_base: float,
    critical_damage_base: float,
):
    return critical_chance_base * (critical_damage_base - 1) + 1


def calculate_damage_cd(
    attack: float,
    skill_multiplier: float,
    damage_ratio: float,
    injury_area: float,
    defence_multiplier: float,
    resistance_area: float,
    damage_reduction: float,
    critical_damage: float,
):
    return (
        attack
        * skill_multiplier
        * damage_ratio
        * injury_area
        * defence_multiplier
        * resistance_area
        * damage_reduction
        * critical_damage
    )


def calculate_damage_qw(
    attack: float,
    skill_multiplier: float,
    damage_ratio: float,
    injury_area: float,
    defence_multiplier: float,
    resistance_area: float,
    damage_reduction: float,
    expected_damage: float,
):
    return (
        attack
        * skill_multiplier
        * damage_ratio
        * injury_area
        * defence_multiplier
        * resistance_area
        * damage_reduction
        * expected_damage
    )


def calculate_damage_tz(
    attack: float,
    skill_multiplier: float,
    damage_ratio: float,
    injury_area: float,
    defence_multiplier: float,
    resistance_area: float,
    damage_reduction: float,
    critical_damage: float,
    element: str,
    element_area: float,
    base_attr: Dict[str, float],
):
    injury_add_tz = 0.0

    attack_tz = attack + 355 + base_attr['attack'] * 2.334
    # logger.info(f'attack_tz: {attack_tz}')
    if element == 'Imaginary':
        injury_add_tz = 0.12
    return (
        attack_tz
        * skill_multiplier
        * damage_ratio
        * (injury_area + injury_add_tz + 2.626)
        * defence_multiplier
        * resistance_area
        * damage_reduction
        * (critical_damage + 1.794)
        * 10
    )
