from __future__ import annotations

from msgspec import convert
from httpx import AsyncClient

from ..utils import _HEADER
from .models import MihomoData


async def get_char_card_info(uid: str) -> MihomoData:
    async with AsyncClient(
        base_url='http://api.mihomo.me',
        headers=_HEADER,
        timeout=30,
    ) as client:
        req = await client.get(f'/sr_info/{uid}')
        return convert(req.json(), type=MihomoData)
