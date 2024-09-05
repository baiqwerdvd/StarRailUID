from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.utils.database.config_switch import set_database_value
from gsuid_core.utils.database.models import GsUser


async def set_config_func(
    uid: str,
    ev: Event,
):
    if "开启" in ev.command:
        if ev.user_type == "direct":
            value = "on"
        elif ev.group_id:
            value = ev.group_id
        else:
            value = "on"
    else:
        value = "off"

    text = await set_database_value(
        GsUser,
        "sr",
        "sr开启",
        ev.text.strip(),
        uid,
        ev.bot_id,
        value,
    )
    if text is None:
        return "[星穹铁道] 未找到配置项"
    logger.success(f"[UID{uid}]成功将配置[SR自动签到]设置为[{value}]!")
    return text
