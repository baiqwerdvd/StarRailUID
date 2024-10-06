from typing import TYPE_CHECKING

from gsuid_core.sv import SV
from gsuid_core.utils.database.api import get_uid
from gsuid_core.utils.error_reply import get_error
from gsuid_core.utils.database.models import GsBind

from ..utils.mys_api import mys_api
from ..utils.error_reply import UID_HINT
from ..utils.name_covert import name_to_avatar_id, alias_to_char_name

if TYPE_CHECKING:
    from gsuid_core.bot import Bot
    from gsuid_core.models import Event

sv_char_calc = SV("sr养成计算")


@sv_char_calc.on_command("养成计算", block=True)
async def send_char_calc_info(bot: "Bot", ev: "Event"):
    name = ev.text.strip()
    char_id = await name_to_avatar_id(name)
    if char_id == "":
        result_fake_name = await alias_to_char_name(name)
        if result_fake_name is None:
            return "请输入正确的角色名"
        fake_name = result_fake_name
        char_id = await name_to_avatar_id(fake_name)

    uid = await get_uid(bot, ev, GsBind, "sr")

    if uid is None:
        return await bot.send(UID_HINT)
    avatar_detail = await mys_api.get_avatar_detail(uid, str(char_id))
    if isinstance(avatar_detail, int):
        return get_error(avatar_detail)
    avatar_skills = avatar_detail.skills + avatar_detail.skills_other
    skill_list = []
    for skill in avatar_skills:
        d = f"{skill.point_id}({skill.cur_level}/{skill.max_level})"
        skill_list.append(d)

    return None
