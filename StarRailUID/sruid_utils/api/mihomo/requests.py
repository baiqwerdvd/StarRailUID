from __future__ import annotations

from pathlib import Path

from httpx import AsyncClient
from msgspec import convert

from ....utils.resource.RESOURCE_PATH import PLAYER_PATH
from ..utils import _HEADER
from .models import MihomoData


async def get_char_card_info(uid: str) -> MihomoData:
    async with AsyncClient(
        base_url='http://api.mihomo.me',
        headers=_HEADER,
        timeout=30,
    ) as client:
        req = await client.get(f'/sr_info/{uid}')
        path = PLAYER_PATH / str(uid)
        path.mkdir(parents=True, exist_ok=True)
        with Path.open(path / f'{uid!s}.json', 'w') as file:
            file.write(req.json())
        return convert(req.json(), type=MihomoData)
