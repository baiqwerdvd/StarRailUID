import json

with open('./data/characters.json', 'r', encoding='utf8') as f:
    characters = json.load(f)

with open('./data/character_ranks.json', 'r', encoding='utf8') as f:
    character_ranks = json.load(f)

with open('./data/character_skills.json', 'r', encoding='utf8') as f:
    character_skills = json.load(f)

with open('./data/character_skill_trees.json', 'r', encoding='utf8') as f:
    character_skill_trees = json.load(f)

with open('./data/AvatarConfig.json', 'r', encoding='utf8') as f:
    AvatarConfig = json.load(f)

with open('./data/TextMapCN.json', 'r', encoding='utf8') as f:
    TextMapCN = json.load(f)

with open('./data/TextMapEN.json', 'r', encoding='utf8') as f:
    TextMapEN = json.load(f)

with open('./data/EquipmentConfig.json', 'r', encoding='utf8') as f:
    EquipmentConfig = json.load(f)

with open('./data/AvatarSkillConfig.json', 'r', encoding='utf8') as f:
    AvatarSkillConfig = json.load(f)

with open('./data/AvatarPropertyConfig.json', 'r', encoding='utf8') as f:
    AvatarPropertyConfig = json.load(f)

with open('./data/EquipmentSkillConfig.json', 'r', encoding='utf8') as f:
    EquipmentSkillConfig = json.load(f)

with open('./data/RelicConfig.json', 'r', encoding='utf8') as f:
    RelicConfig = json.load(f)

with open('./data/RelicSetConfig.json', 'r', encoding='utf8') as f:
    RelicSetConfig = json.load(f)

with open('./data/RelicSetSkillConfig.json', 'r', encoding='utf8') as f:
    RelicSetSkillConfig = json.load(f)

with open('./data/light_cones.json', 'r', encoding='utf8') as f:
    light_cones = json.load(f)

with open('./data/relics_new.json', 'r', encoding='utf8') as f:
    relics_new = json.load(f)

with open('./data/ItemConfigRelic.json', 'r', encoding='utf8') as f:
    ItemConfigRelic = json.load(f)

avatarId2Name = {}
avatarId2EnName = {}
avatarId2DamageType = {}
avatarId2Rarity = {}
rankId2Name = {}
EquipmentID2Name = {}
EquipmentID2EnName = {}
EquipmentID2Rarity = {}
skillId2Name = {}
skillId2Type = {}
Property2Name = {}
Relic2SetId = {}
SetId2Name = {}
characterSkillTree = {}
EquipmentID2AbilityProperty = {}
RelicSetSkill = {}
skillId2AttackType = {}
RelicId2Rarity = {}
ItemId2Name = {}
RelicId2MainAffixGroup = {}

for char in characters:
    char_item = characters[char]
    rank_list = characters[char]['ranks']
    rarity = characters[char]['rarity']
    avatarId2Rarity[char] = str(rarity)
    for rank in rank_list:
        if character_ranks.get(str(rank)):
            eidolon = character_ranks[str(rank)]
            rank_id = eidolon['id']
            rank_name = eidolon['name']
            rankId2Name[rank_id] = rank_name

for item in AvatarConfig:
    avatar_item = AvatarConfig[item]
    avatar_id = avatar_item['AvatarID']
    avatar_name_hash = avatar_item['AvatarName']['Hash']
    avatar_damage_type = avatar_item['DamageType']
    avatar_en_name = ''
    avatar_name = ''
    for item in TextMapCN:
        if str(item) == str(avatar_name_hash):
            avatar_name = TextMapCN[item]
            if avatar_name == '{NICKNAME}':
                avatar_name = '开拓者'
            break
    for item in TextMapEN:
        if str(item) == str(avatar_name_hash):
            avatar_en_name = TextMapEN[item].replace(' ', '')
            break
    avatarId2EnName[avatar_id] = avatar_en_name
    avatarId2Name[avatar_id] = avatar_name
    avatarId2DamageType[avatar_id] = avatar_damage_type


for item in EquipmentConfig:
    equipment_item = EquipmentConfig[item]
    equipment_id = equipment_item['EquipmentID']
    equipment_name_hash = equipment_item['EquipmentName']['Hash']
    equipment_name = ''
    for item in TextMapCN:
        if str(item) == str(equipment_name_hash):
            equipment_name = TextMapCN[item]
            break
    EquipmentID2Name[equipment_id] = equipment_name


for item in EquipmentSkillConfig:
    equipment_item = EquipmentSkillConfig[item]
    EquipmentID2AbilityProperty[str(item)] = {}
    for i in equipment_item:
        equipment_ability_property = equipment_item[str(i)]['AbilityProperty']
        EquipmentID2AbilityProperty[str(item)][i] = equipment_ability_property


for item in EquipmentConfig:
    equipment_item = EquipmentConfig[item]
    equipment_id = equipment_item['EquipmentID']
    equipment_name_hash = equipment_item['EquipmentName']['Hash']
    equipment_name = ''
    for item in TextMapEN:
        if str(item) == str(equipment_name_hash):
            equipment_name = TextMapEN[item].replace(' ', '')
            break
    EquipmentID2EnName[equipment_id] = equipment_name


for skill in AvatarSkillConfig:
    skill_item = AvatarSkillConfig[skill]
    skill_id = skill_item['1']['SkillID']
    skill_name_hash = skill_item['1']['SkillName']['Hash']
    skill_type_hash = skill_item['1']['SkillTag']['Hash']
    skill_attack_type = skill_item['1'].get('AttackType', '')
    skill_name = ''
    skill_type = ''
    for item in TextMapCN:
        if str(item) == str(skill_name_hash):
            skill_name = TextMapCN[item]
            break
    skillId2Name[skill_id] = skill_name
    for item in TextMapCN:
        if str(item) == str(skill_type_hash):
            skill_type = TextMapCN[item]
            break
    skillId2Type[skill_id] = skill_type
    skillId2AttackType[skill_id] = skill_attack_type


for avatar_property in AvatarPropertyConfig:
    PropertyType = AvatarPropertyConfig[avatar_property]['PropertyType']
    PropertyName = AvatarPropertyConfig[avatar_property]['PropertyName']
    PropertyNameHash = AvatarPropertyConfig[avatar_property][
        'PropertyNameFilter'
    ]['Hash']
    Property_Name = ''
    for item in TextMapCN:
        if str(item) == str(PropertyNameHash):
            Property_Name = TextMapCN[item]
            break
    Property2Name[PropertyType] = Property_Name


for relic in RelicConfig:
    Relic2SetId[relic] = RelicConfig[relic]['SetID']
    RelicId2MainAffixGroup[relic] = RelicConfig[relic]['MainAffixGroup']


for set_group in RelicSetConfig:
    set_name_hash = RelicSetConfig[set_group]['SetName']['Hash']
    set_name = ''
    for item in TextMapCN:
        if str(item) == str(set_name_hash):
            set_name = TextMapCN[item]
            break
    SetId2Name[set_group] = set_name


for character in characters:
    char_id = characters[character]['id']
    characterSkillTree[str(char_id)] = (
        {}
        if str(char_id) not in characterSkillTree
        else characterSkillTree[str(char_id)]
    )
    skill_tree_list = characters[character]['skill_trees']
    for skill in skill_tree_list:
        skill_tree = character_skill_trees[skill]
        characterSkillTree[str(char_id)][str(skill)] = skill_tree


for set_ in RelicSetSkillConfig:
    for item in RelicSetSkillConfig[set_]:
        set_id = RelicSetSkillConfig[set_][item]['SetID']
        property_list = RelicSetSkillConfig[set_][item]['PropertyList']
        RelicSetSkill[set_] = (
            {} if set_ not in RelicSetSkill else RelicSetSkill[set_]
        )
        RelicSetSkill[set_][item] = (
            {}
            if item not in RelicSetSkill[set_]
            else RelicSetSkill[set_][item]
        )
        for property_ in property_list:
            property_id = property_['NAOGDGBJNOJ']
            property_value = property_['MBOHKHKHFPD']['Value']
            RelicSetSkill[set_][item]['Property'] = property_id
            RelicSetSkill[set_][item]['Value'] = property_value


for light_cone in light_cones:
    rarity = light_cones[light_cone]['rarity']
    light_cone_id = light_cones[light_cone]['id']
    EquipmentID2Rarity[light_cone_id] = rarity


for item in relics_new:
    rarity = relics_new[item]['rarity']
    relic_id = relics_new[item]['id']
    RelicId2Rarity[relic_id] = rarity

for item in ItemConfigRelic:
    item_id = ItemConfigRelic[item]['ID']
    item_name_hash = ItemConfigRelic[item]['ItemName']['Hash']
    item_name = ''
    for item in TextMapCN:
        if str(item) == str(item_name_hash):
            item_name = TextMapCN[item]
            break
    ItemId2Name[item_id] = item_name


rankId2Name = json.dumps(rankId2Name, ensure_ascii=False)
avatarId2Name = json.dumps(avatarId2Name, ensure_ascii=False)
avatarId2EnName = json.dumps(avatarId2EnName, ensure_ascii=False)
avatarId2DamageType = json.dumps(avatarId2DamageType, ensure_ascii=False)
avatarId2Rarity = json.dumps(avatarId2Rarity, ensure_ascii=False)
EquipmentID2Name = json.dumps(EquipmentID2Name, ensure_ascii=False)
EquipmentID2EnName = json.dumps(EquipmentID2EnName, ensure_ascii=False)
skillId2Name = json.dumps(skillId2Name, ensure_ascii=False)
skillId2Type = json.dumps(skillId2Type, ensure_ascii=False)
Property2Name = json.dumps(Property2Name, ensure_ascii=False)
Relic2SetId = json.dumps(Relic2SetId, ensure_ascii=False)
SetId2Name = json.dumps(SetId2Name, ensure_ascii=False)
characterSkillTree = json.dumps(characterSkillTree, ensure_ascii=False)
EquipmentID2AbilityProperty = json.dumps(
    EquipmentID2AbilityProperty, ensure_ascii=False
)
RelicSetSkill = json.dumps(RelicSetSkill, ensure_ascii=False)
skillId2AttackType = json.dumps(skillId2AttackType, ensure_ascii=False)
EquipmentID2Rarity = json.dumps(EquipmentID2Rarity, ensure_ascii=False)
RelicId2Rarity = json.dumps(RelicId2Rarity, ensure_ascii=False)
ItemId2Name = json.dumps(ItemId2Name, ensure_ascii=False)
RelicId2MainAffixGroup = json.dumps(RelicId2MainAffixGroup, ensure_ascii=False)
print(avatarId2Name)
print(avatarId2EnName)
print(EquipmentID2Name)
print(EquipmentID2EnName)
print(skillId2Name)
print(Property2Name)
print(Relic2SetId)
print(SetId2Name)
print(skillId2Type)
print(rankId2Name)
print(characterSkillTree)
print(avatarId2DamageType)
print(avatarId2Rarity)
print(EquipmentID2AbilityProperty)
print(RelicSetSkill)
print(skillId2AttackType)
print(EquipmentID2Rarity)
print(RelicId2Rarity)
print(ItemId2Name)
print(RelicId2MainAffixGroup)
