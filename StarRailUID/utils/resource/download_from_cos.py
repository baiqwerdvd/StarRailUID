from .RESOURCE_PATH import (
    CHAR_ICON_PATH,
    CHAR_PORTRAIT_PATH,
    CHAR_PREVIEW_PATH,
    CONSUMABLE_PATH,
    ELEMENT_PATH,
    GUIDE_CHARACTER_PATH,
    GUIDE_LIGHT_CONE_PATH,
    RELIC_PATH,
    SKILL_PATH,
    WEAPON_PATH,
    WIKI_LIGHT_CONE_PATH,
    WIKI_MATERIAL_FOR_ROLE,
    WIKI_RELIC_PATH,
    WIKI_ROLE_PATH,
)

from gsuid_core.utils.download_resource.download_core import download_all_file


async def check_use():
    await download_all_file(
        'StarRailUID',
        {
            'resource/character': CHAR_ICON_PATH,
            'resource/character_portrait': CHAR_PORTRAIT_PATH,
            'resource/character_preview': CHAR_PREVIEW_PATH,
            'resource/consumable': CONSUMABLE_PATH,
            'resource/element': ELEMENT_PATH,
            'guide/character_overview': GUIDE_CHARACTER_PATH,
            'guide/light_cone': GUIDE_LIGHT_CONE_PATH,
            'resource/relic': RELIC_PATH,
            'resource/skill': SKILL_PATH,
            'resource/light_cone': WEAPON_PATH,
            'wiki/light_cone': WIKI_LIGHT_CONE_PATH,
            'wiki/character_material': WIKI_MATERIAL_FOR_ROLE,
            'wiki/relic_set': WIKI_RELIC_PATH,
            'wiki/character_overview': WIKI_ROLE_PATH,
        },
    )
    return 'sr全部资源下载完成!'
