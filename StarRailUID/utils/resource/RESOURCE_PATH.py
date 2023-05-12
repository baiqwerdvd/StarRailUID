import sys
from pathlib import Path

from gsuid_core.data_store import get_res_path

MAIN_PATH = get_res_path() / 'StarRailUID'
sys.path.append(str(MAIN_PATH))
CONFIG_PATH = MAIN_PATH / 'config.json'
RESOURCE_PATH = MAIN_PATH / 'resource'
PLAYER_PATH = MAIN_PATH / 'players'
CU_BG_PATH = MAIN_PATH / 'bg'
TEMP_PATH = RESOURCE_PATH / 'temp'
CHAR_ICON_PATH = RESOURCE_PATH / 'character'
WEAPON_PATH = RESOURCE_PATH / 'light_cone'
CHAR_PORTRAIT = RESOURCE_PATH / 'character_portrait'
SKILL_PATH = RESOURCE_PATH / 'skill'
TEXT2D_PATH = Path(__file__).parent / 'texture2d'


def init_dir():
    for i in [
        MAIN_PATH,
        RESOURCE_PATH,
        PLAYER_PATH,
        CHAR_ICON_PATH,
        WEAPON_PATH,
        TEXT2D_PATH,
        CU_BG_PATH,
        TEMP_PATH,
        CHAR_PORTRAIT,
        SKILL_PATH,
    ]:
        i.mkdir(parents=True, exist_ok=True)


init_dir()
