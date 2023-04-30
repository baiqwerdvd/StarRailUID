from io import BytesIO
from typing import List, TypeVar, Generator

from PIL import Image
from aiohttp import ClientSession

T = TypeVar("T")


def wrap_list(lst: List[T], n: int) -> Generator[List[T], None, None]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


async def get_icon(url: str) -> Image.Image:
    async with ClientSession() as client:
        async with client.get(url) as resp:
            return Image.open(BytesIO(await resp.read())).convert("RGBA")
