import re
import json
from typing import Dict, Union, Optional

from gsuid_core.utils.error_reply import CHAR_HINT

from .mono.Character import Character
from ..utils.resource.RESOURCE_PATH import PLAYER_PATH
from ..utils.map.name_covert import name_to_avatar_id, alias_to_char_name


async def draw_char_info_img(raw_mes: str, sr_uid: str, url: Optional[str]):
    # 获取角色名
    char_name = ' '.join(re.findall('[\u4e00-\u9fa5]+', raw_mes))

    char_data = await get_char_data(sr_uid, char_name)
    print(char_data)
    await cal_char_info(char_data)


async def cal_char_info(char_data: dict):
    await Character(char_data).get_equipment_info()


async def get_char_data(
    sr_uid: str, char_name: str, enable_self: bool = True
) -> Union[Dict, str]:
    player_path = PLAYER_PATH / str(sr_uid)
    SELF_PATH = player_path / 'SELF'
    print(char_name)
    char_id = await name_to_avatar_id(char_name)
    print(char_id)
    if '开拓者' in char_name:
        char_name = '开拓者'
    else:
        char_name = await alias_to_char_name(char_id, char_name)

    char_path = player_path / f'{char_name}.json'
    char_self_path = SELF_PATH / f'{char_name}.json'

    if char_path.exists():
        path = char_path
    elif enable_self and char_self_path.exists():
        path = char_self_path
    else:
        return CHAR_HINT.format(char_name)

    with open(path, 'r', encoding='utf8') as fp:
        char_data = json.load(fp)
    return char_data
