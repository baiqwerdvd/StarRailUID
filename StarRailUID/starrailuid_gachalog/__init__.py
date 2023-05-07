from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from ..utils.convert import get_uid
from ..utils.error_reply import UID_HINT

# from .get_gachalogs import save_gachalogs
# from .draw_gachalogs import draw_gachalogs_img

sv_gacha_log = SV('sr抽卡记录')


@sv_gacha_log.on_fullmatch(('sr抽卡记录'))
async def send_gacha_log_card_info(bot: Bot, ev: Event):
    await bot.logger.info('开始执行[sr抽卡记录]')
    uid, user_id = await get_uid(bot, ev, True)
    if uid is None:
        return await bot.send(UID_HINT)
    # im = await draw_gachalogs_img(uid, user_id)
    im = '画个饼先，在做了在做了'
    await bot.send(im)
