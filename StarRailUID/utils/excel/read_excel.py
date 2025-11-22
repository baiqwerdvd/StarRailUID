import hashlib
import json
from pathlib import Path

import aiohttp

EXCEL = Path(__file__).parent
LIGHT_CONE_FILE = EXCEL / "light_cone_ranks.json"

# 初始化读取
with LIGHT_CONE_FILE.open(encoding="utf8") as f:
    light_cone_ranks = json.load(f)


async def update_light_cone_ranks():
    global light_cone_ranks  # 允许修改模块级变量
    base = "https://starrail.wget.es"
    async with aiohttp.ClientSession() as s:
        v = await (await s.get(f"{base}/version.json")).json()
        remote_sha = v["files"]["light_cone_ranks.json"]["sha256"]
        local_sha = (
            hashlib.sha256(LIGHT_CONE_FILE.read_bytes()).hexdigest()
            if LIGHT_CONE_FILE.exists()
            else None
        )

        if local_sha != remote_sha:
            ver = v["version"]
            data = await (await s.get(f"{base}/{ver}/light_cone_ranks.json")).read()
            if hashlib.sha256(data).hexdigest() == remote_sha:
                LIGHT_CONE_FILE.parent.mkdir(parents=True, exist_ok=True)
                LIGHT_CONE_FILE.write_bytes(data)
                light_cone_ranks = json.loads(data.decode("utf8"))
                msg = "光锥评价已更新并重新加载"
            else:
                pmsg = "数据校验失败"
        else:
            msg = "光锥评价数据已是最新版本"
    return msg
