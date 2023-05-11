from mpmath import mp

from ..utils.excel.read_excel import RelicSubAffix, RelicMainAffix

mp.dps = 14


async def cal_relic_main_affix(
    relic_id: int, affix_id: int, relic_type: int, relic_level: int
):
    rarity = int(str(relic_id)[0]) - 1
    group = str(rarity) + str(relic_type)
    relic_data = RelicMainAffix[group][str(affix_id)]
    assert relic_data['GroupID'] == int(group)
    assert relic_data['AffixID'] == affix_id
    base_value = mp.mpf(relic_data['BaseValue']['Value'])
    level_add = mp.mpf(relic_data['LevelAdd']['Value'])
    value = base_value + level_add * relic_level
    affix_property = relic_data['Property']
    return affix_property, str(value)


async def cal_relic_sub_affix(
    relic_id: int, affix_id: int, cnt: int, step: int
):
    rarity = int(str(relic_id)[0]) - 1
    relic_data = RelicSubAffix[str(rarity)][str(affix_id)]
    assert relic_data['GroupID'] == int(rarity)
    assert relic_data['AffixID'] == affix_id
    base_value = mp.mpf(relic_data['BaseValue']['Value'])
    step_value = mp.mpf(relic_data['StepValue']['Value'])
    value = base_value * cnt + step_value * step
    affix_property = relic_data['Property']
    return affix_property, str(value)
