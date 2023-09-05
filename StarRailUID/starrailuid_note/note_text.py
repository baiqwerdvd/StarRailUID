from datetime import datetime

from ..utils.mys_api import mys_api
from ..utils.error_reply import get_error

month_im = """==============
SR_UID:{}
==============
本日获取星琼:{}
本日获取星轨通票&星轨专票:{}
==============
昨日获取星琼:{}
昨日获取星轨通票&星轨专票:{}
==============
本月获取星琼:{}
本月获取星轨通票&星轨专票:{}
==============
上月获取星琼:{}
上月获取星轨通票&星轨专票:{}
==============
星琼收入组成:
{}=============="""


async def award(uid) -> str:
    # 获取当前的月份
    data = await mys_api.get_award(uid, datetime.now().month)
    if isinstance(data, int):
        return get_error(data)
    day_hcoin = data['day_data']['current_hcoin']
    day_rails_pass = data['day_data']['current_rails_pass']
    lastday_hcoin = 0
    lastday_rails_pass = 0
    if int(uid[0]) < 6:
        lastday_hcoin = data['day_data']['last_hcoin']
        lastday_rails_pass = data['day_data']['last_rails_pass']
    month_stone = data['month_data']['current_hcoin']
    month_rails_pass = data['month_data']['current_rails_pass']
    lastmonth_stone = data['month_data']['last_hcoin']
    lastmonth_rails_pass = data['month_data']['last_rails_pass']
    group_str = ''
    for i in data['month_data']['group_by']:
        group_str = (
            group_str
            + i['action_name']
            + ':'
            + str(i['num'])
            + '('
            + str(i['percent'])
            + '%)'
            + '\n'
        )

    return month_im.format(
        uid,
        day_hcoin,
        day_rails_pass,
        lastday_hcoin,
        lastday_rails_pass,
        month_stone,
        month_rails_pass,
        lastmonth_stone,
        lastmonth_rails_pass,
        group_str,
    )
