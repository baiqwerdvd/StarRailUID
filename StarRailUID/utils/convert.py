from typing import Optional, Tuple, Union

from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.utils.database.api import get_uid as get_uid_db
from gsuid_core.utils.database.models import GsBind


async def get_uid(
    bot: Bot, ev: Event, get_user_id: bool = False
) -> Union[Optional[str], Tuple[Optional[str], str]]:
    return await get_uid_db(bot, ev, GsBind, "sr", get_user_id)  # type: ignore
