from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .note_text import award
from ..utils.api import get_sqla
from ..utils.convert import get_uid
from ..utils.sr_prefix import PREFIX
from ..utils.error_reply import UID_HINT
from .draw_note_card import draw_note_img

sv_get_monthly_data = SV('sr查询月历')


# 群聊内 每月统计 功能
@sv_get_monthly_data.on_fullmatch(f'{PREFIX}每月统计')
async def send_monthly_data(bot: Bot, ev: Event):
    sqla = get_sqla(ev.bot_id)
    sr_uid = await sqla.get_bind_sruid(ev.user_id)
    if sr_uid is None:
        return UID_HINT
    await bot.send(await award(sr_uid))
    return None


@sv_get_monthly_data.on_fullmatch(
    (f'{PREFIX}开拓月历', f'{PREFIX}zj', f'{PREFIX}月历')
)
async def send_monthly_pic(bot: Bot, ev: Event):
    await bot.logger.info('开始执行[sr开拓月历]')
    sr_uid = await get_uid(bot, ev)
    if sr_uid is None:
        return UID_HINT
    im = await draw_note_img(str(sr_uid))
    await bot.send(im)
    return None
