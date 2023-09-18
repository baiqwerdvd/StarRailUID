from ..utils.map.SR_MAP_PATH import RelicId2MainAffixGroup
from ..utils.excel.model import RelicSubAffixConfig, RelicMainAffixConfig


async def cal_relic_main_affix(
    relic_id: int,
    set_id: str,
    affix_id: int,
    relic_type: int,
    relic_level: int,
):
    if set_id[0] == 3:
        rarity = int(str(relic_id)[0]) - 1
        group_id = str(rarity) + str(relic_type)
    else:
        group_id = str(RelicId2MainAffixGroup[str(relic_id)])
    relic_data = RelicMainAffixConfig.Relic[group_id][str(affix_id)]
    base_value = relic_data.BaseValue.Value
    level_add = relic_data.LevelAdd.Value
    value = base_value + level_add * relic_level
    affix_property = relic_data.Property
    return affix_property, value


async def cal_relic_sub_affix(
    relic_id: int, affix_id: int, cnt: int, step: int
):
    rarity = int(str(relic_id)[0]) - 1
    relic_data = RelicSubAffixConfig.Relic[str(rarity)][str(affix_id)]
    base_value = relic_data.BaseValue.Value
    step_value = relic_data.StepValue.Value
    value = base_value * cnt + step_value * step
    affix_property = relic_data.Property
    return affix_property, value
