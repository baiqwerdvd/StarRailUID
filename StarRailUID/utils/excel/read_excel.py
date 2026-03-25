import hashlib
import json
from pathlib import Path
from typing import Any

import aiohttp
from gsuid_core.logger import logger

EXCEL = Path(__file__).parent
LIGHT_CONE_FILE = EXCEL / "light_cone_ranks.json"

# 初始化读取
with LIGHT_CONE_FILE.open(encoding="utf8") as f:
    light_cone_ranks = json.load(f)


async def update_light_cone_ranks():
    base = "https://starrail.wget.es"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base}/version.json") as resp:
                resp.raise_for_status()
                version_data = await resp.json()

            file_info = version_data.get("files", {}).get("light_cone_ranks.json")
            remote_sha = str(file_info["sha256"]) if isinstance(file_info, dict) else ""
            if not remote_sha:
                return "光锥评价版本信息缺失"

            local_sha = (
                hashlib.sha256(LIGHT_CONE_FILE.read_bytes()).hexdigest()
                if LIGHT_CONE_FILE.exists()
                else None
            )
            if local_sha == remote_sha:
                return "光锥评价数据已是最新版本"

            version = str(version_data["version"])
            async with session.get(f"{base}/{version}/light_cone_ranks.json") as resp:
                resp.raise_for_status()
                data = await resp.read()
    except Exception:
        logger.exception("更新光锥评价数据时出错")
        return "光锥评价更新失败"

    if hashlib.sha256(data).hexdigest() != remote_sha:
        logger.warning("光锥评价数据校验失败")
        return "光锥评价数据校验失败"

    try:
        parsed_data: dict[str, Any] = json.loads(data.decode("utf8"))
        LIGHT_CONE_FILE.parent.mkdir(parents=True, exist_ok=True)
        LIGHT_CONE_FILE.write_bytes(data)
    except Exception:
        logger.exception("写入光锥评价数据时出错")
        return "光锥评价更新失败"

    light_cone_ranks.clear()
    light_cone_ranks.update(parsed_data)
    return "光锥评价已更新并重新加载"
