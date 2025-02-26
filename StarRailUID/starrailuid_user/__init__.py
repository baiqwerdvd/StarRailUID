from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV
from gsuid_core.utils.database.models import GsBind

from .draw_user_card import get_user_card
from ..utils.message import send_diff_msg

sv_user_config = SV("sr用户管理", pm=2)
sv_user_info = SV("sr用户信息")


@sv_user_info.on_fullmatch("绑定信息")
async def send_bind_card(bot: Bot, ev: Event):
    logger.info("sr开始执行[查询用户绑定状态]")
    uid_list = await get_user_card(ev.bot_id, ev.user_id)
    if not uid_list:
        return await bot.send("你还没有绑定SR_UID哦!")
    logger.info("sr[查询用户绑定状态]完成!等待图片发送中...")
    await bot.send(uid_list)
    return None


@sv_user_info.on_command(
    (
        "绑定uid",
        "绑定UID",
        "切换uid",
        "切换UID",
        "删除uid",
        "删除UID",
        "解绑uid",
        "解绑UID",
    )
)
async def send_link_uid_msg(bot: Bot, ev: Event):
    logger.info("sr开始执行[绑定/解绑用户信息]")
    qid = ev.user_id
    logger.info(f"sr[绑定/解绑]UserID: {qid}")

    sr_uid = ev.text.strip()
    if sr_uid and not sr_uid.isdigit():
        return await bot.send("你输入了错误的格式!")

    if "绑定" in ev.command:
        data = await GsBind.insert_uid(qid, ev.bot_id, sr_uid, ev.group_id, 9, game_name="sr")
        return await send_diff_msg(
            bot,
            data,
            {
                0: f"✅[崩铁]绑定UID{sr_uid}成功!",
                -1: f"❌SR_UID{sr_uid}的位数不正确!",
                -2: f"❌SR_UID{sr_uid}已经绑定过了!",
                -3: "❌你输入了错误的格式!",
            },
        )

    if "切换" in ev.command:
        data = await GsBind.switch_uid_by_game(qid, ev.bot_id, sr_uid, "sr")
        return await send_diff_msg(
            bot,
            data,
            {
                0: f"✅[崩铁]切换uid{sr_uid}成功!",
                -1: "❌[崩铁]不存在绑定记录!",
                -2: "❌[崩铁]请绑定两个以上UID再进行切换!",
                -3: "❌[崩铁]请绑定两个以上UID再进行切换!",
            },
        )

    data = await GsBind.delete_uid(qid, ev.bot_id, sr_uid, "sr")
    return await send_diff_msg(
        bot,
        data,
        {
            0: f"✅[崩铁]删除UID{sr_uid}成功!",
            -1: f"❌[崩铁]该UID{sr_uid}不在已绑定列表中!",
        },
    )
