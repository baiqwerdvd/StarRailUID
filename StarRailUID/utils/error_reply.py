from copy import deepcopy

from gsuid_core.utils.error_reply import ERROR_CODE
from gsuid_core.sv import get_plugin_available_prefix

prefix = get_plugin_available_prefix("StarRailUID")

UID_HINT = f"你还没有绑定过uid哦!\n请使用[{prefix}绑定uid123456]命令绑定!"
_CHAR_HINT = f"再使用【{prefix}强制刷新】命令来缓存数据进行查询! !"
CHAR_HINT = "您的支援/星海同行角色没有{}的数据哦!\n请先把{}放入支援/星海同行中" + _CHAR_HINT


SR_ERROR_CODE = deepcopy(ERROR_CODE)


def get_error(retcode: int) -> str:
    msg_list = [f'❌错误代码为: {retcode}']
    if retcode in SR_ERROR_CODE:
        msg_list.append(f'📝错误信息: {SR_ERROR_CODE[retcode]}')
    return '\n'.join(msg_list)
