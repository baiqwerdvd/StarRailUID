from typing import Dict, Union

from msgspec import convert
from httpx import AsyncClient

from ..utils import _HEADER
from .model import (
    HakushHsrCharacter,
    HakushHsrLightcone,
    HakushHsrCharacterIndex,
    HakushHsrLightconeIndex,
)


async def get_character_data(
    avatar_id: str,
) -> Union[HakushHsrCharacter, None]:
    async with AsyncClient(
        base_url="https://api.hakush.in/hsr/data",
        headers=_HEADER,
        timeout=30,
    ) as client:
        req = await client.get(f"/cn/character/{avatar_id}.json")
        if req.status_code == 200:
            return convert(req.json(), type=HakushHsrCharacter)
        return None


async def get_lightcone_data(
    lightcone_id: str,
) -> Union[HakushHsrLightcone, None]:
    async with AsyncClient(
        base_url="https://api.hakush.in/hsr/data",
        headers=_HEADER,
        timeout=30,
    ) as client:
        req = await client.get(f"/cn/lightcone/{lightcone_id}.json")
        if req.status_code == 200:
            return convert(req.json(), type=HakushHsrLightcone)
        return None


async def get_character_index() -> Union[Dict[str, HakushHsrCharacterIndex], None]:
    async with AsyncClient(
        base_url="https://api.hakush.in/hsr/data",
        headers=_HEADER,
        timeout=30,
    ) as client:
        req = await client.get("/character.json")
        if req.status_code == 200:
            return convert(req.json(), type=Dict[str, HakushHsrCharacterIndex])
        return None


async def get_lightcone_index() -> Union[Dict[str, HakushHsrLightconeIndex], None]:
    async with AsyncClient(
        base_url="https://api.hakush.in/hsr/data",
        headers=_HEADER,
        timeout=30,
    ) as client:
        req = await client.get("/character.json")
        if req.status_code == 200:
            return convert(req.json(), type=Dict[str, HakushHsrLightconeIndex])
        return None
