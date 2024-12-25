from typing import Union
from gsuid_core.handler import command_start

if command_start and command_start[0]:
    _start = command_start[0]
else:
    _start = ''

UID_HINT = f"你还没有绑定过uid哦!\n请使用[{_start}sr绑定uid123456]命令绑定!"
MYS_HINT = f"你还没有绑定过mysid哦!\n请使用[{_start}绑定mys1234]命令绑定!"
CK_HINT = """你还没有绑定过Cookie哦!发送【ck帮助】获取帮助!
警告:绑定Cookie可能会带来未知的账号风险,请确保信任机器人管理员"""

_CHAR_HINT = f"再使用【{_start}sr强制刷新】命令来缓存数据进行查询! "
CHAR_HINT = "您的支援/星海同行角色没有{}的数据哦!\n请先把{}放入支援/星海同行中!" + _CHAR_HINT
VERIFY_HINT = """出现验证码!
如已绑定CK: 请至米游社软件->我的->我的角色处解锁验证码
(可使用[gs关闭推送]命令关闭体力推送以减少出现验证码风险)
如未绑定CK: 可联系管理员使用[gs清除缓存]命令
"""
SK_HINT = "你还没有绑定过Stoken或者Stoken已失效~\n请群聊发送 [扫码登陆] 或加好友私聊Bot [添加]后跟SK格式 以绑定SK"
UPDATE_HINT = """更新失败!更多错误信息请查看控制台...
>> 可以尝试使用
>> [gs强制更新](危险)
>> [gs强行强制更新](超级危险)!"""


def get_error(retcode: Union[int, str]) -> str:
    if retcode == -51:
        return CK_HINT
    if retcode == -100:
        return "您的cookie已经失效, 请重新获取!"
    if retcode == 10001:
        return "您的cookie已经失效, 请重新获取!"
    if retcode == 10101:
        return "当前查询CK已超过每日30次上限!"
    if retcode == 10102:
        return "当前查询id已经设置了隐私, 无法查询!"
    if retcode == 1034:
        return VERIFY_HINT
    if retcode == -10001:
        return "请求体出错, 请检查具体实现代码..."
    if retcode == 10104:
        return CK_HINT
    if retcode == -512009:
        return "[留影叙佳期]已经获取过该内容~!"
    if retcode == -201:
        return "你的账号可能已被封禁, 请联系米游社客服..."
    if retcode == -501101:
        return "当前角色冒险等阶未达到10级, 暂时无法参加此活动..."
    if retcode == 400:
        return "[MINIGG]暂未找到此内容..."
    if retcode == -400:
        return "请输入更详细的名称..."
    return f"API报错, 错误码为{retcode}!"
