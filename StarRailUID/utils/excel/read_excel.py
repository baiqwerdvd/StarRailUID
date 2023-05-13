import json
from pathlib import Path

EXCEL = Path(__file__).parent

with open(EXCEL / 'RelicMainAffixConfig.json', 'r', encoding='utf8') as f:
    RelicMainAffix = json.load(f)

with open(EXCEL / 'RelicSubAffixConfig.json', 'r', encoding='utf8') as f:
    RelicSubAffix = json.load(f)

with open(EXCEL / 'AvatarPromotionConfig.json', 'r', encoding='utf8') as f:
    AvatarPromotion = json.load(f)

with open(EXCEL / 'EquipmentPromotionConfig.json', 'r', encoding='utf8') as f:
    EquipmentPromotion = json.load(f)

with open(EXCEL / 'light_cone_ranks.json', 'r', encoding='utf8') as f:
    light_cone_ranks = json.load(f)
