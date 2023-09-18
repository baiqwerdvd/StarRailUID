from typing import List

from gsuid_core.logger import logger

from ..utils.error_reply import get_error
from ..utils.mys_api import mys_api

daily_im = '''*数据刷新可能存在一定延迟,请以当前游戏实际数据为准
==============
开拓力:{}/{}{}
委托执行:
总数/完成/上限:{}/{}/{}
{}'''


def seconds2hours(seconds: int) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return '%02d:%02d:%02d' % (h, m, s)


async def get_stamina_text(uid: str) -> str:
    try:
        dailydata = await mys_api.get_daily_data(uid)
        if isinstance(dailydata, int):
            return get_error(dailydata)
        max_stamina = dailydata['max_stamina']
        rec_time = ''
        current_stamina = dailydata['current_stamina']
        if current_stamina < 160:
            stamina_recover_time = seconds2hours(
                dailydata['stamina_recover_time']
            )
            next_stamina_rec_time = seconds2hours(
                8 * 60
                - (
                    (dailydata['max_stamina'] - dailydata['current_stamina'])
                    * 8
                    * 60
                    - int(dailydata['stamina_recover_time'])
                )
            )
            rec_time = f' ({next_stamina_rec_time}/{stamina_recover_time})'

        accepted_epedition_num = dailydata['accepted_expedition_num']
        total_expedition_num = dailydata['total_expedition_num']
        finished_expedition_num = 0
        expedition_info: List[str] = []
        for expedition in dailydata['expeditions']:
            expedition_name = expedition['name']

            if expedition['status'] == 'Finished':
                expedition_info.append(f'{expedition_name} 探索完成')
                finished_expedition_num += 1
            else:
                remaining_time: str = seconds2hours(
                    expedition['remaining_time']
                )
                expedition_info.append(
                    f'{expedition_name} 剩余时间{remaining_time}'
                )

        expedition_data = '\n'.join(expedition_info)
        return daily_im.format(
            current_stamina,
            max_stamina,
            rec_time,
            accepted_epedition_num,
            finished_expedition_num,
            total_expedition_num,
            expedition_data,
        )
    except TypeError:
        logger.exception('[查询当前状态]查询失败!')
        return '你绑定过的UID中可能存在过期CK~请重新绑定一下噢~'
