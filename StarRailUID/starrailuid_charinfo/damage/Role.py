from typing import List, Union

from gsuid_core.logger import logger

from .utils import merge_attribute


async def demage_num(
    base_attr,
    attribute_bonus,
    skill_type,
    add_skill_type,
    element,
    skill_multiplier,
    level,
):
    logger.info(f'技能区: {skill_multiplier}')
    logger.info(f'skill_type: {skill_type}')
    logger.info(f'level: {level}')
    # logger.info(f'base_attr: {base_attr}')
    # logger.info(f'attribute_bonus: {attribute_bonus}')
    # 检查是否有对某一个技能的属性加成
    logger.info('检查是否有对某一个技能的属性加成')
    for attr in attribute_bonus:
        # 攻击加成
        if attr.__contains__('AttackAddedRatio'):
            attr_name = attr.split('AttackAddedRatio')[0]
            if attr_name in (skill_type, add_skill_type):
                attack_added_ratio = attribute_bonus.get('AttackAddedRatio', 0)
                attribute_bonus['AttackAddedRatio'] = (
                    attack_added_ratio + attribute_bonus[attr]
                )
        # 效果命中加成
        if attr.__contains__('StatusProbabilityBase'):
            attr_name = attr.split('StatusProbabilityBase')[0]
            if attr_name in (skill_type, add_skill_type):
                status_probability = attribute_bonus.get(
                    'StatusProbabilityBase', 0
                )
                attribute_bonus['StatusProbabilityBase'] = (
                    status_probability + attribute_bonus[attr]
                )

    merged_attr = await merge_attribute(base_attr, attribute_bonus)
    # logger.info(f'{merged_attr}')
    skill_info_list = []
    attack = merged_attr.get('attack', 0)
    logger.info(f'攻击力: {attack}')
    damage_add = 0

    # 模拟 同属性弱点 同等级 的怪物
    # 韧性条减伤
    enemy_damage_reduction = 0.1
    damage_reduction = 1 - enemy_damage_reduction
    logger.info(f'韧性区: {damage_reduction}')
    # 抗性区
    enemy_status_resistance = 0.0
    for attr in merged_attr:
        if attr.__contains__('ResistancePenetration'):
            # 检查是否有某一属性的抗性穿透
            attr_name = attr.split('ResistancePenetration')[0]
            if attr_name in (element, 'AllDamage'):
                logger.info(f'{attr_name}属性有{merged_attr[attr]}穿透加成')
                enemy_status_resistance += merged_attr[attr]
            # 检查是否有某一技能属性的抗性穿透
            if attr_name.__contains__('_'):
                skill_name = attr_name.split('_')[0]
                skillattr_name = attr_name.split('_')[1]
                if skill_name in (
                    skill_type,
                    add_skill_type,
                ) and skillattr_name in (element, 'AllDamage'):
                    enemy_status_resistance += merged_attr[attr]
                    logger.info(
                        f'{skill_name}对{skillattr_name}属性有{merged_attr[attr]}穿透加成'
                    )
    resistance_area = 1.0 - (0 - enemy_status_resistance)
    logger.info(f'抗性区: {resistance_area}')

    # 防御区
    # 检查是否有 ignore_defence
    logger.info('检查是否有 ignore_defence')
    ignore_defence = 1.0
    for attr in merged_attr:
        if attr == 'ignore_defence':
            ignore_defence = 1 - merged_attr[attr]
            break
    logger.info(f'ignore_defence {ignore_defence}')
    enemy_defence = (level * 10 + 200) * ignore_defence
    defence_multiplier = (level * 10 + 200) / (
        level * 10 + 200 + enemy_defence
    )
    logger.info(f'防御区: {defence_multiplier}')

    # 增伤区
    injury_area = 0
    # 检查是否有对某一个技能的伤害加成
    # logger.info('检查是否有对某一个技能的伤害加成')
    for attr in merged_attr:
        if attr.__contains__('DmgAdd'):
            attr_name = attr.split('DmgAdd')[0]
            if attr_name in (skill_type, add_skill_type):
                logger.info(
                    f'{attr} 对 {skill_type} 有 {merged_attr[attr]} 伤害加成'
                )
                injury_area += merged_attr[attr]
    # 检查有无符合属性的伤害加成
    # logger.info('检查球有无符合属性的伤害加成')
    element_area = 0
    for attr in merged_attr:
        if attr.__contains__('AddedRatio'):
            attr_name = attr.split('AddedRatio')[0]
            if attr_name in (element, 'AllDamage'):
                logger.info(
                    f'{attr} 对 {element} 有 {merged_attr[attr]} 伤害加成'
                )
                if attr_name == element:
                    element_area += merged_attr[attr]
                injury_area += merged_attr[attr]
    injury_area += 1
    logger.info(f'增伤区: {injury_area}')

    # 易伤区
    # logger.info('检查是否有易伤加成')
    damage_ratio = merged_attr.get('DmgRatio', 0)
    # 检查是否有对特定技能的易伤加成
    # Talent_DmgRatio
    for attr in merged_attr:
        if attr.__contains__('_DmgRatio'):
            skill_name = attr.split('_')[0]
            if skill_name in (skill_type, add_skill_type):
                logger.info(
                    f'{attr} 对 {skill_type} 有 {merged_attr[attr]} 易伤加成'
                )
                damage_ratio += merged_attr[attr]
    damage_ratio = damage_ratio + 1
    logger.info(f'易伤: {damage_ratio}')

    # 爆伤区
    if skill_type == 'DOT':
        critical_damage_base = 0.0
    else:
        # logger.info('检查是否有爆伤加成')
        # logger.info(f'{merged_attr}')
        critical_damage_base = merged_attr.get('CriticalDamageBase', 0)
        # 检查是否有对特定技能的爆伤加成
        # Ultra_CriticalChance
        for attr in merged_attr:
            if attr.__contains__('_CriticalDamageBase'):
                skill_name = attr.split('_')[0]
                if skill_name in (skill_type, add_skill_type):
                    logger.info(
                        f'{attr} 对 {skill_type} 有 {merged_attr[attr]} 爆伤加成'
                    )
                    critical_damage_base += merged_attr[attr]
    critical_damage = critical_damage_base + 1
    logger.info(f'暴伤: {critical_damage}')

    # 暴击区
    logger.info('检查是否有暴击加成')
    critical_chance_base = merged_attr['CriticalChanceBase']
    # 检查是否有对特定技能的爆伤加成
    # Ultra_CriticalChance
    for attr in merged_attr:
        if attr.__contains__('_CriticalChance'):
            skill_name = attr.split('_')[0]
            if skill_name in (skill_type, add_skill_type):
                logger.info(
                    f'{attr} 对 {skill_type} 有 {merged_attr[attr]} 暴击加成'
                )
                critical_chance_base += merged_attr[attr]
    critical_chance_base = min(1, critical_chance_base)
    logger.info(f'暴击: {critical_chance_base}')

    # 期望伤害
    qiwang_damage = (critical_chance_base * critical_damage_base) + 1
    logger.info(f'暴击期望: {qiwang_damage}')

    attack_tz = 0.0
    injury_add = 0.0
    critical_damage_add = 0

    damage_cd = (
        attack
        * skill_multiplier
        * damage_ratio
        * (injury_area + injury_add)
        * defence_multiplier
        * resistance_area
        * damage_reduction
        * (critical_damage + critical_damage_add)
        + damage_add
    )

    damage_qw = (
        attack
        * skill_multiplier
        * damage_ratio
        * (injury_area + injury_add)
        * defence_multiplier
        * resistance_area
        * damage_reduction
        * qiwang_damage
        + damage_add
    )

    attr_value_tz: float = base_attr.get('attack', 0)
    attribute_atk = attribute_bonus.get('AttackDelta', 0)
    attack_tz = (
        attr_value_tz
        + attr_value_tz
        * (1 + attribute_bonus.get('AttackAddedRatio', 0) + 2.144)
        + attribute_atk
    )

    injury_add_tz = 0

    if element == 'Imaginary':
        injury_add_tz = 0.12

    damage_tz = (
        attack_tz
        * skill_multiplier
        * damage_ratio
        * (injury_area + injury_add + injury_add_tz + 2.326)
        * defence_multiplier
        * resistance_area
        * damage_reduction
        * (critical_damage + critical_damage_add + 1.594)
        * 10
        + damage_add
    )

    if element == 'Thunder':
        element_area = 0
    damage_tz_fj = (
        attack_tz
        * 0.44
        * damage_ratio
        * (injury_area + injury_add + 2.326 + element_area)
        * defence_multiplier
        * resistance_area
        * damage_reduction
        * (critical_damage + critical_damage_add + 1.594)
        * 10
    )
    damage_tz += damage_tz_fj
    skill_info_list: List[Union[str, float]] = []
    skill_info_list.append(damage_cd)
    skill_info_list.append(damage_qw)
    skill_info_list.append(damage_tz)
    logger.info(f'暴击: {damage_cd} 期望：{damage_qw}  末日：{damage_tz}')
    return skill_info_list
