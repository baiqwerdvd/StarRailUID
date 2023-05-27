import asyncio
import threading

from gsuid_core.logger import logger

from ..utils.api import get_sqla
from ..starrailuid_resource import startup


async def all_start():
    try:
        get_sqla('TEMP')
        await startup()
    except Exception as e:
        logger.exception(e)


threading.Thread(target=lambda: asyncio.run(all_start()), daemon=True).start()
