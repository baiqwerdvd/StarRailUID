import json
from pathlib import Path
from typing import List, Union

import msgspec
from msgspec import json as msgjson

from ..sruid_utils.api.mihomo.models import Character
from ..sruid_utils.api.mihomo.requests import get_char_card_info


async def api_to_dict(
    uid: Union[str, None] = None,
    save_path: Union[Path, None] = None,
) -> list[str]:
    if not uid:
        raise KeyError
    sr_data = await get_char_card_info(uid)

    player = sr_data.player
    characters = sr_data.characters

    if save_path and uid:
        path = save_path / uid
        path.mkdir(parents=True, exist_ok=True)
        with Path.open(path / f"{uid!s}.json", "wb") as file:
            file.write(msgjson.format(msgjson.encode(sr_data), indent=4))
        with Path.open(path / "rawData.json", "wb") as file:
            file.write(msgjson.format(msgjson.encode(sr_data), indent=4))

    player_uid = str(player.uid)

    char_name_list: List[str] = []
    char_id_list: List[str] = []
    for char in characters:
        if str(char.id) in char_id_list:
            continue
        char_data, avatarName = await get_data(
            char,
            player_uid,
            save_path,
        )
        char_name_list.append(avatarName)
        char_id_list.append(str(char.id))

    return char_id_list


async def get_data(
    char: Character, uid: str, save_path: Union[Path, None] = None
):
    avatarName = char.name
    char_data = msgspec.json.encode(char).decode("utf-8")
    if save_path:
        path = save_path / str(uid)
        path.mkdir(parents=True, exist_ok=True)
        path.mkdir(parents=True, exist_ok=True)
        with Path.open(path / f"{avatarName}.json", "w", encoding="UTF-8") as file:
            file.write(char_data)
    return char, avatarName
