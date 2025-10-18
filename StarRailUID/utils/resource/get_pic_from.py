from io import BytesIO
from pathlib import Path
from typing import TypeVar

from PIL import Image
from gsuid_core.data_store import get_res_path
from httpx import AsyncClient

T = TypeVar("T")

ROLEINFO_PATH = get_res_path() / "StarRailUID" / "roleinfo"
ROLEINFO_PATH.mkdir(parents=True, exist_ok=True)

ABYSSPEAK_PATH = get_res_path() / "StarRailUID" / "abysspeak"
ABYSSPEAK_PATH.mkdir(parents=True, exist_ok=True)


async def get_roleinfo_icon(url: str) -> Image.Image:
    name = url.split("/")[-1]
    path = ROLEINFO_PATH / name
    if (path).exists():
        content = path.read_bytes()
    else:
        async with AsyncClient() as client:
            resp = await client.get(url)
            content = resp.read()
            with Path.open(path, "wb") as f:
                f.write(content)
    return Image.open(BytesIO(content)).convert("RGBA")


async def get_abyss_peak_img(name: str, url: str) -> Image.Image:
    path = ABYSSPEAK_PATH / name
    if (path).exists():
        content = path.read_bytes()
    else:
        async with AsyncClient() as client:
            resp = await client.get(url)
            content = resp.read()
            with Path.open(path, "wb") as f:
                f.write(content)
    return Image.open(BytesIO(content)).convert("RGBA")