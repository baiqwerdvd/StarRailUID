import copy
from typing import Dict, Union, Literal, Optional, cast

from gsuid_core.utils.api.mys import MysApi
from gsuid_core.utils.api.mys.models import MysSign, SignInfo
from gsuid_core.utils.api.mys.tools import (
    random_hex,
    generate_os_ds,
    get_web_ds_token,
)

from ..utils.database import get_sqla
from ..sruid_utils.api.mys.api import _API
from ....GenshinUID.GenshinUID.genshinuid_config.gs_config import gsconfig

mysVersion = '2.44.1'
_HEADER = {
    'x-rpc-app_version': mysVersion,
    'User-Agent': (
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) '
        f'AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/{mysVersion}'
    ),
    'x-rpc-client_type': '5',
    'Referer': 'https://webstatic.mihoyo.com/',
    'Origin': 'https://webstatic.mihoyo.com',
}


class _MysApi(MysApi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _pass(self, gt: str, ch: str, header: Dict):
        # 警告：使用该服务（例如某RR等）需要注意风险问题
        # 本项目不以任何形式提供相关接口
        # 代码来源：GITHUB项目MIT开源
        _pass_api = gsconfig.get_config('_pass_API').data
        if _pass_api:
            data = await self._mys_request(
                url=f'{_pass_api}&gt={gt}&challenge={ch}',
                method='GET',
                header=header,
            )
            if isinstance(data, int):
                return None, None
            else:
                validate = data['data']['validate']
                ch = data['data']['challenge']
        else:
            validate = None

        return validate, ch

    async def _upass(self, header: Dict, is_bbs: bool = False):
        if is_bbs:
            raw_data = await self.get_bbs_upass_link(header)
        else:
            raw_data = await self.get_upass_link(header)
        if isinstance(raw_data, int):
            return False
        gt = raw_data['data']['gt']
        ch = raw_data['data']['challenge']

        vl, ch = await self._pass(gt, ch, header)

        if vl:
            await self.get_header_and_vl(header, ch, vl)
        else:
            return True

    async def get_ck(
        self, uid: str, mode: Literal['OWNER', 'RANDOM'] = 'RANDOM'
    ) -> Optional[str]:
        sqla = get_sqla('TEMP')
        if mode == 'RANDOM':
            return await sqla.get_random_cookie(uid)
        else:
            return await sqla.get_user_cookie(uid)

    async def get_stoken(self, uid: str) -> Optional[str]:
        sqla = get_sqla('TEMP')
        return await sqla.get_user_stoken(uid)

    async def get_sign_info(self, uid) -> Union[SignInfo, int]:
        # server_id = RECOGNIZE_SERVER.get(str(uid)[0])
        is_os = self.check_os(uid)
        if is_os:
            params = {
                'act_id': 'e202304121516551',
                'lang': 'zh-cn',
            }
            header = {
                'DS': generate_os_ds(),
            }
        else:
            params = {
                'act_id': 'e202304121516551',
                'lang': 'zh-cn',
            }
            header = {}
        data = await self._mys_req_get(
            'STAR_RAIL_SIGN_INFO_URL', is_os, params, header
        )
        if isinstance(data, Dict):
            data = cast(SignInfo, data['data'])
        return data

    async def mys_sign(
        self, uid, header={}, server_id='cn_gf01'
    ) -> Union[MysSign, int]:
        ck = await self.get_ck(uid, 'OWNER')
        if ck is None:
            return -51
        if int(str(uid)[0]) < 6:
            HEADER = copy.deepcopy(_HEADER)
            HEADER['Cookie'] = ck
            HEADER['x-rpc-device_id'] = random_hex(32)
            HEADER['x-rpc-app_version'] = '2.44.1'
            HEADER['x-rpc-client_type'] = '5'
            HEADER['X_Requested_With'] = 'com.mihoyo.hyperion'
            HEADER['DS'] = get_web_ds_token(True)
            HEADER['Referer'] = (
                'https://webstatic.mihoyo.com/bbs/event/signin/hkrpg'
                '/mys_sign?act_id=e202304121516551&bbs_auth_required=true'
                '&bbs_presentation_style=fullscreen&utm_source=share'
                '&utm_medium=bbs&utm_campaign=app'
            )
            HEADER.update(header)
            data = await self._mys_request(
                url=_API['SIGN_URL'],
                method='POST',
                header=HEADER,
                data={
                    'act_id': 'e202304121516551',
                    'lang': 'zh-cn',
                },
            )
        else:
            pass
        if isinstance(data, Dict):
            data = cast(MysSign, data['data'])
        return data


mys_api = _MysApi()
