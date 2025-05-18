
from gsuid_core.logger import logger

from ..starrailuid_resource import startup
from gsuid_core.server import on_core_start

@on_core_start
async def all_start():
    try:
        await startup()
    except Exception as e:
        logger.exception(e)