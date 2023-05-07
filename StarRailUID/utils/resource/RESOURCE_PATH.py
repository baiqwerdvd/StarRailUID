import sys

from gsuid_core.data_store import get_res_path

MAIN_PATH = get_res_path() / 'StarRailUID'
sys.path.append(str(MAIN_PATH))
CONFIG_PATH = MAIN_PATH / 'config.json'
RESOURCE_PATH = MAIN_PATH / 'resource'
PLAYER_PATH = MAIN_PATH / 'players'
CHAR_PATH = RESOURCE_PATH / 'chars'
WEAPON_PATH = RESOURCE_PATH / 'weapons'


def init_dir():
    for i in [MAIN_PATH, RESOURCE_PATH, PLAYER_PATH, CHAR_PATH, WEAPON_PATH]:
        i.mkdir(parents=True, exist_ok=True)


init_dir()
