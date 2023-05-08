import sys
from pathlib import Path

from gsuid_core.data_store import get_res_path

MAIN_PATH = get_res_path() / 'StarRailUID'
sys.path.append(str(MAIN_PATH))
CONFIG_PATH = MAIN_PATH / 'config.json'
RESOURCE_PATH = MAIN_PATH / 'resource'
PLAYER_PATH = MAIN_PATH / 'players'
CU_BG_PATH = MAIN_PATH / 'bg'
CHAR_ICON_PATH = RESOURCE_PATH / 'char_icon'
WEAPON_PATH = RESOURCE_PATH / 'weapons'
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
    ]:
        i.mkdir(parents=True, exist_ok=True)


init_dir()
