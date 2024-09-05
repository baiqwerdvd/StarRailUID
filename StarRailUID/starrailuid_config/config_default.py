from typing import Dict

from gsuid_core.utils.plugins_config.models import (
    GSC,
    GsBoolConfig,
    GsIntConfig,
    GsListStrConfig,
    GsStrConfig,
)

CONIFG_DEFAULT: Dict[str, GSC] = {
    "SignTime": GsListStrConfig(
        "每晚签到时间设置", "每晚米游社签到时间设置(时,分)", ["0", "38"]
    ),
    "PrivateSignReport": GsBoolConfig(
        "签到私聊报告",
        "关闭后将不再给任何人推送当天签到任务完成情况",
        False,
    ),
    "SchedSignin": GsBoolConfig(
        "定时签到",
        "开启后每晚00:30将开始自动签到任务",
        True,
    ),
    "SchedStaminaPush": GsBoolConfig(
        "定时检查开拓力",
        "开启后每隔半小时检查一次开拓力",
        True,
    ),
    "push_max_value": GsIntConfig("提醒阈值", "发送提醒的阈值", 200, 240),
    "CrazyNotice": GsBoolConfig(
        "催命模式",
        "开启后当达到推送阈值将会一直推送",
        False,
    ),
    "StarRailPrefix": GsStrConfig(
        "插件命令前缀(确认无冲突再修改)",
        "用于本插件的前缀设定",
        "sr",
    ),
    "WidgetResin": GsBoolConfig(
        "体力使用组件API",
        "开启后mr功能将转为调用组件API, 可能缺失数据、数据不准",
        True,
    ),
}
