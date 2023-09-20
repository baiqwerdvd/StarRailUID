import re
from typing import Tuple, Union, Optional, overload

from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .api import get_sqla


@overload
async def get_uid(
    bot: Bot, ev: Event, get_user_id: bool = False, only_uid: bool = False
) -> Optional[str]:
    ...


@overload
async def get_uid(
    bot: Bot, ev: Event, get_user_id: bool = True, only_uid: bool = False
) -> Tuple[Optional[str], str]:
    ...


async def get_uid(
    bot: Bot, ev: Event, get_user_id: bool = False, only_uid: bool = False
) -> Union[Optional[str], Tuple[Optional[str], str]]:
    uid_data = re.findall(r'\d{9}', ev.text)
    user_id = ev.at if ev.at else ev.user_id
    if uid_data:
        sr_uid: Optional[str] = uid_data[0]
        if sr_uid:
            ev.text = ev.text.replace(sr_uid, '')
    else:
        sqla = get_sqla(ev.bot_id)
        sr_uid = await sqla.get_bind_sruid(user_id)
    if only_uid:
        sqla = get_sqla(ev.bot_id)
        sr_uid = await sqla.get_bind_sruid(user_id)
    if get_user_id:
        return sr_uid, user_id
    return sr_uid
