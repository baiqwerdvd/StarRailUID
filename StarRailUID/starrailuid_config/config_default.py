from typing import Dict

from gsuid_core.utils.plugins_config.models import (
    GSC,
    GsBoolConfig,
    GsListStrConfig,
    GsStrConfig,
)

CONIFG_DEFAULT: Dict[str, GSC] = {
    'SignTime': GsListStrConfig('每晚签到时间设置', '每晚米游社签到时间设置(时,分)', ['0', '38']),
    'SignReportSimple': GsBoolConfig(
        '简洁签到报告',
        '开启后可以大大减少每日签到报告字数',
        True,
    ),
    'SchedSignin': GsBoolConfig(
        '定时签到',
        '开启后每晚00:30将开始自动签到任务',
        True,
    ),
    'CrazyNotice': GsBoolConfig(
        '催命模式',
        '开启后当达到推送阈值将会一直推送',
        False,
    ),
    'StarRailPrefix': GsStrConfig(
        '插件命令前缀(确认无冲突再修改)',
        '用于本插件的前缀设定',
        'sr',
    ),
    'WidgetResin': GsBoolConfig(
        '体力使用组件API',
        '开启后mr功能将转为调用组件API, 可能缺失数据、数据不准',
        True,
    ),
}
