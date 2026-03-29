from gsuid_core.logger import logger
from httpx import AsyncClient
from msgspec import convert

from .models import MihomoData
from ..utils import _HEADER
from ....utils.resource.RESOURCE_PATH import PLAYER_PATH


async def get_char_card_info(uid: str) -> MihomoData:
    async with AsyncClient(
        base_url="http://api.mihomo.me",
        headers=_HEADER,
        timeout=30,
        follow_redirects=True,
    ) as client:
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                req = await client.get(f"/sr_info/{uid}")
                req.raise_for_status()
                path = PLAYER_PATH / str(uid)
                path.mkdir(parents=True, exist_ok=True)
                (path / f"{uid}.json").write_text(req.text, encoding="utf-8")
                return convert(req.json(), type=MihomoData)
            except Exception as exc:
                last_error = exc
                logger.warning(f"[sr面板] mihomo 请求失败, attempt={attempt + 1}, uid={uid}, error={exc}")
        raise RuntimeError(f"mihomo 面板获取失败: UID{uid}") from last_error
