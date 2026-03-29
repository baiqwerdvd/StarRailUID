from io import BytesIO
from pathlib import Path

from PIL import Image
from gsuid_core.data_store import get_res_path
from gsuid_core.logger import logger
from httpx import AsyncClient

ROLEINFO_PATH = get_res_path() / "StarRailUID" / "roleinfo"
ROLEINFO_PATH.mkdir(parents=True, exist_ok=True)

ABYSSPEAK_PATH = get_res_path() / "StarRailUID" / "abysspeak"
ABYSSPEAK_PATH.mkdir(parents=True, exist_ok=True)


def _read_cached_image_bytes(path: Path) -> bytes | None:
    if path.exists():
        return path.read_bytes()
    return None


def _write_cached_image_bytes(path: Path, content: bytes) -> None:
    path.write_bytes(content)


async def _read_remote_image_bytes(url: str) -> bytes:
    last_error: Exception | None = None
    for attempt in range(2):
        try:
            async with AsyncClient(timeout=30, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as exc:
            last_error = exc
            logger.warning(f"[sr资源] 图片下载失败, attempt={attempt + 1}, url={url}, error={exc}")
    raise RuntimeError(f"图片下载失败: {url}") from last_error


async def _get_cached_image(path: Path, url: str) -> Image.Image:
    content = _read_cached_image_bytes(path)
    if content is None:
        content = await _read_remote_image_bytes(url)
        _write_cached_image_bytes(path, content)
    return Image.open(BytesIO(content)).convert("RGBA")


async def get_roleinfo_icon(url: str) -> Image.Image:
    name = url.split("/")[-1]
    path = ROLEINFO_PATH / name
    return await _get_cached_image(path, url)


async def get_abyss_peak_img(name: str, url: str) -> Image.Image:
    path = ABYSSPEAK_PATH / name
    return await _get_cached_image(path, url)
