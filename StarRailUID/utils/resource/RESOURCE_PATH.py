from pathlib import Path
import sys

from gsuid_core.data_store import get_res_path

MAIN_PATH = get_res_path() / "StarRailUID"
sys.path.append(str(MAIN_PATH))

CU_BG_PATH = MAIN_PATH / "bg"
CONFIG_PATH = MAIN_PATH / "config.json"
PLAYER_PATH = MAIN_PATH / "players"
RESOURCE_PATH = MAIN_PATH / "resource"
WIKI_PATH = MAIN_PATH / "wiki"
GUIDE_PATH = MAIN_PATH / "guide"

CHAR_ICON_PATH = RESOURCE_PATH / "character"
CHAR_PORTRAIT_PATH = RESOURCE_PATH / "character_portrait"
CONSUMABLE_PATH = RESOURCE_PATH / "consumable"
ELEMENT_PATH = RESOURCE_PATH / "element"
WEAPON_PATH = RESOURCE_PATH / "light_cone"
RELIC_PATH = RESOURCE_PATH / "relic"
SKILL_PATH = RESOURCE_PATH / "skill"
TEMP_PATH = RESOURCE_PATH / "temp"
CHAR_PREVIEW_PATH = RESOURCE_PATH / "character_preview"

WIKI_LIGHT_CONE_PATH = WIKI_PATH / "light_cone"
WIKI_MATERIAL_FOR_ROLE = WIKI_PATH / "character_material"
WIKI_RELIC_PATH = WIKI_PATH / "relic_set"
WIKI_ROLE_PATH = WIKI_PATH / "character_overview"

GUIDE_LIGHT_CONE_PATH = GUIDE_PATH / "light_cone"
GUIDE_CHARACTER_PATH = GUIDE_PATH / "character_overview"

TEXT2D_PATH = Path(__file__).parent / "texture2d"


def init_dir():
    for i in [
        MAIN_PATH,
        CU_BG_PATH,
        PLAYER_PATH,
        RESOURCE_PATH,
        WIKI_PATH,
        GUIDE_PATH,
        CHAR_ICON_PATH,
        CHAR_PORTRAIT_PATH,
        CHAR_PREVIEW_PATH,
        CONSUMABLE_PATH,
        ELEMENT_PATH,
        WEAPON_PATH,
        RELIC_PATH,
        SKILL_PATH,
        TEXT2D_PATH,
        TEMP_PATH,
        WIKI_LIGHT_CONE_PATH,
        WIKI_MATERIAL_FOR_ROLE,
        WIKI_RELIC_PATH,
        WIKI_ROLE_PATH,
        GUIDE_LIGHT_CONE_PATH,
        GUIDE_CHARACTER_PATH,
    ]:
        i.mkdir(parents=True, exist_ok=True)


init_dir()
