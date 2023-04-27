from typing import List

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from ..utils.api import get_sqla

# from .qrlogin import qrcode_login
# from .get_ck_help_msg import get_ck_help
from ..utils.message import send_diff_msg
from .draw_user_card import get_user_card

# from gsuid_core.segment import MessageSegment

# from .add_ck import deal_ck, get_ck_by_stoken, get_ck_by_all_stoken

sv_user_config = SV('sr用户管理', pm=2)
sv_user_add = SV('sr用户添加')
# sv_user_qrcode_login = SV('sr扫码登陆')
# sv_user_addck = SV('sr添加CK', area='DIRECT')
sv_user_info = SV('sr用户信息')
# sv_user_help = SV('sr绑定帮助')


# @sv_user_config.on_fullmatch(('sr刷新全部CK', 'sr刷新全部ck'))
# async def send_refresh_all_ck_msg(bot: Bot, ev: Event):
#     await bot.logger.info('sr开始执行[刷新全部CK]')
#     im = await get_ck_by_all_stoken(ev.bot_id)
#     await bot.send(im)
#
#
# @sv_user_add.on_fullmatch(('sr刷新CK', 'sr刷新ck'))
# async def send_refresh_ck_msg(bot: Bot, ev: Event):
#     await bot.logger.info('sr开始执行[刷新CK]')
#     im = await get_ck_by_stoken(ev.bot_id, ev.user_id)
#     await bot.send(im)


# @sv_user_qrcode_login.on_fullmatch(('sr扫码登陆', 'sr扫码登录'))
# async def send_qrcode_login(bot: Bot, ev: Event):
#     await bot.logger.info('sr开始执行[扫码登陆]')
#     im = await qrcode_login(bot, ev, ev.user_id)
#     if not im:
#         return
#     im = await deal_ck(ev.bot_id, im, ev.user_id)
#     await bot.send(im)


@sv_user_info.on_fullmatch(('sr绑定信息'))
async def send_bind_card(bot: Bot, ev: Event):
    await bot.logger.info('sr开始执行[查询用户绑定状态]')
    # im = await get_user_card(ev.bot_id, ev.user_id)
    uid_list = await get_user_card(ev.bot_id, ev.user_id)
    await bot.logger.info('sr[查询用户绑定状态]完成!等待图片发送中...')
    await bot.send(uid_list)


# @sv_user_addck.on_prefix(('sr添加'))
# async def send_add_ck_msg(bot: Bot, ev: Event):
#     im = await deal_ck(ev.bot_id, ev.text, ev.user_id)
#     await bot.send(im)


@sv_user_info.on_command(('sr绑定uid', 'sr切换uid', 'sr删除uid', 'sr解绑uid'))
async def send_link_uid_msg(bot: Bot, ev: Event):
    await bot.logger.info('sr开始执行[绑定/解绑用户信息]')
    qid = ev.user_id
    await bot.logger.info('sr[绑定/解绑]UserID: {}'.format(qid))

    sqla = get_sqla(ev.bot_id)
    sr_uid = ev.text.strip()
    if sr_uid and not sr_uid.isdigit():
        return await bot.send('你输入了错误的格式!')

    if ev.command.startswith('sr绑定'):
        data = await sqla.insert_bind_data(qid, sr_uid=sr_uid)
        print(data)
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
    elif ev.command.startswith('sr切换'):
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


# @sv_user_help.on_fullmatch(('ck帮助', '绑定帮助'))
# async def send_ck_help(bot: Bot, ev: Event):
#     msg_list = await get_ck_help()
#     await bot.send(MessageSegment.node(msg_list))
