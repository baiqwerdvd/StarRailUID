from typing import Dict

from gsuid_core.logger import logger


async def merge_attribute(
    base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
) -> Dict[str, float]:
    merged_attr = base_attr.copy()
    for attribute, value in attribute_bonus.items():
        if attribute.endswith('Delta'):
            attr = attribute.split('Delta')[0].lower()
            if attr in merged_attr:
                merged_attr[attr] += value
            else:
                merged_attr[attribute] = attribute_bonus[attribute]
        elif attribute.endswith('AddedRatio'):
            attr = attribute.split('AddedRatio')[0].lower()
            if attr in merged_attr:
                merged_attr[attr] += base_attr[attr] * value
            else:
                merged_attr[attribute] = attribute_bonus[attribute]
        elif attribute in [
            'ignore_defence',
            'Atk_buff',
            'Normal_buff',
            'shield_added_ratio',
        ]:
            merged_attr[attribute] = base_attr.get(attribute, 0) + value
        elif attribute.endswith(
            ('ResistancePenetration', 'DmgAdd', 'DmgRatio')
        ):
            merged_attr[attribute] = base_attr.get(attribute, 0) + value
        elif attribute.endswith('Base'):
            merged_attr[attribute] = base_attr.get(attribute, 0) + value
        else:
            logger.info(f'未知的属性加成: {attribute}, 采用覆盖模式')
            merged_attr[attribute] = attribute_bonus[attribute]
    return merged_attr

def merge_attribute_dam(
    base_attr: Dict[str, float], attribute_bonus: Dict[str, float]
) -> Dict[str, float]:
    merged_attr = base_attr.copy()
    for attribute, value in attribute_bonus.items():
        if attribute.endswith('Delta'):
            attr = attribute.split('Delta')[0].lower()
            if attr in merged_attr:
                merged_attr[attr] += value
            else:
                merged_attr[attribute] = attribute_bonus[attribute]
        elif attribute.endswith('AddedRatio'):
            attr = attribute.split('AddedRatio')[0].lower()
            if attr in merged_attr:
                merged_attr[attr] += base_attr[attr] * value
            else:
                merged_attr[attribute] = attribute_bonus[attribute]
        elif attribute in [
            'ignore_defence',
            'Atk_buff',
            'Normal_buff',
            'shield_added_ratio',
        ]:
            merged_attr[attribute] = base_attr.get(attribute, 0) + value
        elif attribute.endswith(
            ('ResistancePenetration', 'DmgAdd', 'DmgRatio')
        ):
            merged_attr[attribute] = base_attr.get(attribute, 0) + value
        elif attribute.endswith('Base'):
            merged_attr[attribute] = base_attr.get(attribute, 0) + value
        else:
            logger.info(f'未知的属性加成: {attribute}, 采用覆盖模式')
            merged_attr[attribute] = attribute_bonus[attribute]
    return merged_attr