import json
from collections import Counter
from typing import Dict

from loguru import logger
from mpmath import mp

from ....utils.map.SR_MAP_PATH import EquipmentID2AbilityProperty, RelicSetSkill

mp.dps = 14

class Character:
    def __init__(self, card_prop: Dict):
        # 面板数据
        self.card_prop: Dict = card_prop

        self.char_level: int = int(card_prop['avatarLevel'])
        self.char_id: str = card_prop['avatarId']
        self.char_name: str = card_prop['avatarName']
        self.char_rank = card_prop['rank'] if card_prop.get('rank') else 0
        self.char_rarity = card_prop['avatarRarity']
        self.char_element = card_prop['avatarElement']
        self.char_promotion = card_prop['avatarPromotion']
        self.char_skill = card_prop['avatarSkill']
        self.extra_ability = card_prop['avatarExtraAbility']
        self.attribute_bonus = card_prop['avatarAttributeBonus']
        self.char_relic = card_prop['RelicInfo']
        self.base_attributes = card_prop['baseAttributes']
        self.add_attr = {}
        self.equipment = card_prop['equipmentInfo']
        self.rarity = card_prop['avatarRarity']
        self.eidolons = (
            card_prop['rankList'] if card_prop.get('rankList') else []
        )

        # 伤害计算
        self.def_ignore = 0
        self.q_dmg = 0
        self.q_crit_dmg = 0
        self.e_dmg = 0
        self.a_dmg = 0
        self.a3_dmg = 0

        # 角色的圣遗物总分
        self.artifacts_all_score: float = 0
        self.percent: str = '0.0'
        self.dmg_data: Dict = {}
        self.seq_str: str = '无匹配'

    async def get_equipment_info(self):
        if self.equipment == {}:
            return
        base_attr = self.base_attributes
        equip = self.equipment
        ability_property = EquipmentID2AbilityProperty[
            str(equip['equipmentID'])
        ]
        equip_rank = equip['equipmentRank']

        equip_ability_property = ability_property[str(equip_rank)]

        equip_add_base_attr = equip['baseAttributes']
        hp = mp.mpf(base_attr['hp']) + mp.mpf(equip_add_base_attr['hp'])
        attack = mp.mpf(base_attr['attack']) + mp.mpf(
            equip_add_base_attr['attack']
        )
        defence = mp.mpf(base_attr['defence']) + mp.mpf(
            equip_add_base_attr['defence']
        )
        base_attr['hp'] = str(hp)
        base_attr['attack'] = str(attack)
        base_attr['defence'] = str(defence)
        self.base_attributes = base_attr

        for equip_ability in equip_ability_property:
            property_type = equip_ability['PropertyType']
            value = equip_ability['Value']['Value']
            if property_type in self.add_attr:
                self.add_attr[property_type] += value
            else:
                self.add_attr[property_type] = value

    async def get_char_attribute_bonus(self):
        attribute_bonus = self.attribute_bonus
        for bonus in attribute_bonus:
            status_add = bonus['statusAdd']
            bonus_property = status_add['property']
            value = status_add['value']
            if bonus_property in self.add_attr:
                self.add_attr[bonus_property] += value
            else:
                self.add_attr[bonus_property] = value

    async def get_relic_info(self):
        # 计算圣遗物效果
        set_id_list = []
        for relic in self.char_relic:
            set_id_list.append(relic['SetId'])
            # 处理主属性
            relic_property = relic['MainAffix']['Property']
            property_value = mp.mpf(relic['MainAffix']['Value'])
            if relic_property in self.add_attr:
                self.add_attr[relic_property] = str(
                    mp.mpf(self.add_attr[relic_property]) + property_value
                )
            else:
                self.add_attr[relic_property] = str(property_value)
            # 处理副词条
            for sub in relic['SubAffixList']:
                sub_property = sub['Property']
                sub_value = mp.mpf(sub['Value'])
                if sub_property in self.add_attr:
                    self.add_attr[sub_property] = str(
                        mp.mpf(self.add_attr[sub_property]) + sub_value
                    )
                else:
                    self.add_attr[sub_property] = str(sub_value)
        # 处理套装属性
        set_id_dict = Counter(set_id_list)
        for item in set_id_dict.most_common():
            set_property = ''
            set_id = item[0]
            count = item[1]
            set_value = 0
            if count >= 2 and RelicSetSkill[str(set_id)]['2'] != {}:
                set_property = RelicSetSkill[str(set_id)]['2']['Property']
                set_value = mp.mpf(RelicSetSkill[str(set_id)]['2']['Value'])
            if count == 4 and RelicSetSkill[str(set_id)]['4'] != {}:
                set_property = RelicSetSkill[str(set_id)]['4']['Property']
                set_value = mp.mpf(RelicSetSkill[str(set_id)]['4']['Value'])
            if set_property != '':
                if set_property in self.add_attr:
                    self.add_attr[set_property] = str(
                        mp.mpf(self.add_attr[set_property]) + set_value
                    )
                else:
                    self.add_attr[set_property] = str(set_value)

        logger.info(json.dumps(self.base_attributes))
        logger.info(json.dumps(self.add_attr))