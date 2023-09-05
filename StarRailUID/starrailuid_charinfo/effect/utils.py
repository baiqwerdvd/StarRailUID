from typing import Dict


async def merge_attribute(base_attr: Dict, attribute_bonus: Dict) -> Dict:
    # hp attack defence need base_value and add_value
    merged_attr = {}
    for attribute in attribute_bonus:
        if (
            attribute.__contains__('Attack')
            or attribute.__contains__('Defence')
            or attribute.__contains__('HP')
            or attribute.__contains__('Speed')
        ):
            if attribute.__contains__('Delta'):
                attr = attribute.split('Delta')[0].lower()
                attr_value = merged_attr.get(attr, 0)
                merged_attr[attr] = attr_value + attribute_bonus[attribute]
            elif attribute.__contains__('AddedRatio'):
                attr = attribute.split('AddedRatio')[0].lower()
                attr_value = merged_attr.get(attr, 0)
                merged_attr[attr] = attr_value + base_attr[attr] * (
                    1 + attribute_bonus[attribute]
                )
            else:
                raise Exception(f'attribute error {attribute}')
        elif attribute.__contains__('Base'):
            attr_value = base_attr.get(attribute, 0)
            merged_attr[attribute] = attr_value + attribute_bonus[attribute]
        elif attribute.__contains__('AddedRatio'):
            # attr = attribute.split('AddedRatio')[0]
            attr_value = base_attr.get(attribute, 0)
            merged_attr[attribute] = attr_value + attribute_bonus[attribute]
        elif attribute.__contains__('DmgAdd'):
            attr_value = base_attr.get(attribute, 0)
            merged_attr[attribute] = attr_value + attribute_bonus[attribute]
        elif attribute.__contains__('DmgRatio'):
            attr_value = base_attr.get(attribute, 0)
            merged_attr[attribute] = attr_value + attribute_bonus[attribute]
        elif attribute == 'ignore_defence':
            attr_value = base_attr.get(attribute, 0)
            merged_attr[attribute] = attr_value + attribute_bonus[attribute]
        elif attribute.__contains__('ResistancePenetration'):
            attr_value = base_attr.get(attribute, 0)
            merged_attr[attribute] = attr_value + attribute_bonus[attribute]
        elif attribute == 'Atk_buff':
            attr_value = base_attr.get(attribute, 0)
            merged_attr[attribute] = attr_value + attribute_bonus[attribute]
        elif attribute == 'Normal_buff':
            attr_value = base_attr.get(attribute, 0)
            merged_attr[attribute] = attr_value + attribute_bonus[attribute]
        else:
            raise Exception(f'attribute error {attribute}')
    return merged_attr
