from __future__ import annotations

from typing import Dict

from httpx import AsyncClient

# from .models import EnkaData


async def get_char_card_info(uid: str) -> Dict:
    async with AsyncClient(
        base_url='https://mhy.fuckmys.tk',
        timeout=30,
    ) as client:
        req = await client.get(f'/sr_info/{uid}')
        return req.json()