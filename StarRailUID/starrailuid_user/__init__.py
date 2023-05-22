from typing import List

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from ..utils.api import get_sqla
from ..utils.sr_prefix import PREFIX
from ..utils.message import send_diff_msg
from .draw_user_card import get_user_card

sv_user_config = SV('sr用户管理', pm=2)
sv_user_add = SV('sr用户添加')
sv_user_info = SV('sr用户信息')
# sv_user_help = SV('sr绑定帮助')


@sv_user_info.on_fullmatch((f'{PREFIX}绑定信息'))
async def send_bind_card(bot: Bot, ev: Event):
    await bot.logger.info('sr开始执行[查询用户绑定状态]')
    uid_list = await get_user_card(ev.bot_id, ev.user_id)
    await bot.logger.info('sr[查询用户绑定状态]完成!等待图片发送中...')
    await bot.send(uid_list)


@sv_user_info.on_command(
    (f'{PREFIX}绑定uid', f'{PREFIX}切换uid', f'{PREFIX}删除uid', f'{PREFIX}解绑uid')
)
async def send_link_uid_msg(bot: Bot, ev: Event):
    await bot.logger.info('sr开始执行[绑定/解绑用户信息]')
    qid = ev.user_id
    await bot.logger.info('sr[绑定/解绑]UserID: {}'.format(qid))

    sqla = get_sqla(ev.bot_id)
    sr_uid = ev.text.strip()
    if sr_uid and not sr_uid.isdigit():
        return await bot.send('你输入了错误的格式!')

    if '绑定' in ev.command:
        data = await sqla.insert_bind_data(qid, sr_uid=sr_uid)
        return await send_diff_msg(
            bot,
            data,
            {
                0: f'绑定SR_UID{sr_uid}成功！',
                -1: f'SR_UID{sr_uid}的位数不正确！',
                -2: f'SR_UID{sr_uid}已经绑定过了！',
                -3: '你输入了错误的格式!',
            },
        )
    elif '切换' in ev.command:
        data = await sqla.switch_uid(qid, uid=sr_uid)
        if isinstance(data, List):
            return await bot.send(f'切换SR_UID{sr_uid}成功！')
        else:
            return await bot.send(f'尚未绑定该SR_UID{sr_uid}')
    else:
        data = await sqla.delete_bind_data(qid, sr_uid=sr_uid)
        return await send_diff_msg(
            bot,
            data,
            {
                0: f'删除SR_UID{sr_uid}成功！',
                -1: f'该SR_UID{sr_uid}不在已绑定列表中！',
            },
        )
