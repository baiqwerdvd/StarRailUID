import copy
import random
from string import digits, ascii_letters
from typing import Dict, Union, Literal, Optional, cast

from gsuid_core.utils.api.mys.request import BaseMysApi
from gsuid_core.utils.api.mys.models import MysSign, SignInfo, SignList
from gsuid_core.utils.api.mys.tools import (
    random_hex,
    get_ds_token,
    generate_os_ds,
    get_web_ds_token,
)

from ..utils.api import get_sqla
from ..sruid_utils.api.mys.api import _API
from ....GenshinUID.GenshinUID.genshinuid_config.gs_config import gsconfig
from ..sruid_utils.api.mys.models import (
    MonthlyAward,
    DailyNoteData,
    RoleBasicInfo,
)

RECOGNIZE_SERVER = {
    '1': 'prod_gf_cn',
    # '2': 'cn_gf01',
    # '5': 'cn_qd01',
    # '6': 'os_usa',
    # '7': 'os_euro',
    # '8': 'os_asia',
    # '9': 'os_cht',
}


class _MysApi(BaseMysApi):
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

    async def create_qrcode_url(self) -> Union[Dict, int]:
        device_id: str = ''.join(random.choices(ascii_letters + digits, k=64))
        app_id: str = '8'
        data = await self._mys_request(
            _API['CREATE_QRCODE'],
            'POST',
            header={},
            data={'app_id': app_id, 'device': device_id},
        )
        if isinstance(data, Dict):
            url: str = data['data']['url']
            ticket = url.split('ticket=')[1]
            return {
                'app_id': app_id,
                'ticket': ticket,
                'device': device_id,
                'url': url,
            }
        return data

    async def get_daily_data(self, uid: str) -> Union[DailyNoteData, int]:
        data = await self.simple_mys_req('STAR_RAIL_NOTE_URL', uid)
        if isinstance(data, Dict):
            data = cast(DailyNoteData, data['data'])
        return data

    async def get_sign_list(self, uid) -> Union[SignList, int]:
        # is_os = self.check_os(uid)
        is_os = False
        if is_os:
            params = {
                'act_id': 'e202304121516551',
                'lang': 'zh-cn',
            }
        else:
            params = {
                'act_id': 'e202304121516551',
                'lang': 'zh-cn',
            }
        data = await self._mys_req_get(
            'STAR_RAIL_SIGN_LIST_URL', is_os, params
        )
        if isinstance(data, Dict):
            data = cast(SignList, data['data'])
        return data

    async def get_sign_info(self, uid) -> Union[SignInfo, int]:
        # server_id = RECOGNIZE_SERVER.get(str(uid)[0])
        # is_os = self.check_os(uid)
        is_os = False
        if is_os:
            # TODO
            params = {
                'act_id': 'e202304121516551',
                'lang': 'zh-cn',
                'region': 'prod_gf_cn',
                'uid': uid,
            }
            header = {
                'DS': generate_os_ds(),
            }
        else:
            params = {
                'act_id': 'e202304121516551',
                'lang': 'zh-cn',
                'region': 'prod_gf_cn',
                'uid': uid,
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
            HEADER = copy.deepcopy(self._HEADER)
            HEADER['Cookie'] = ck
            HEADER['x-rpc-device_id'] = random_hex(32)
            HEADER['x-rpc-app_version'] = '2.44.1'
            HEADER['x-rpc-client_type'] = '5'
            HEADER['X_Requested_With'] = 'com.mihoyo.hyperion'
            HEADER['DS'] = get_web_ds_token(True)
            HEADER['Referer'] = 'https://webstatic.mihoyo.com'
            HEADER.update(header)
            data = await self._mys_request(
                url=_API['STAR_RAIL_SIGN_URL'],
                method='POST',
                header=HEADER,
                data={
                    'act_id': 'e202304121516551',
                    'region': 'prod_gf_cn',
                    'uid': uid,
                    'lang': 'zh-cn',
                },
            )
        else:
            pass
        if isinstance(data, Dict):
            data = cast(MysSign, data['data'])
        return data

    async def get_award(self, sr_uid) -> Union[MonthlyAward, int]:
        server_id = RECOGNIZE_SERVER.get(str(sr_uid)[0])
        ck = await self.get_ck(sr_uid, 'OWNER')
        if ck is None:
            return -51
        if int(str(sr_uid)[0]) < 6:
            HEADER = copy.deepcopy(self._HEADER)
            HEADER['Cookie'] = ck
            HEADER['DS'] = get_web_ds_token(True)
            HEADER['x-rpc-device_id'] = random_hex(32)
            data = await self._mys_request(
                url=_API['STAR_RAIL_MONTH_INFO_URL'],
                method='GET',
                header=HEADER,
                params={'uid': sr_uid, 'region': server_id, 'month': ''},
            )
        else:
            HEADER = copy.deepcopy(self._HEADER_OS)
            HEADER['Cookie'] = ck
            HEADER['x-rpc-device_id'] = random_hex(32)
            HEADER['DS'] = generate_os_ds()
            data = await self._mys_request(
                url=_API['STAR_RAIL_MONTH_INFO_URL'],
                method='GET',
                header=HEADER,
                params={'uid': sr_uid, 'region': server_id, 'month': ''},
                use_proxy=True,
            )
        if isinstance(data, Dict):
            data = cast(MonthlyAward, data['data'])
        return data

    async def get_role_basic_info(
        self, sr_uid: str
    ) -> Union[RoleBasicInfo, int]:
        data = await self.simple_mys_req(
            'STAR_RAIL_ROLE_BASIC_INFO_URL', sr_uid
        )
        if isinstance(data, Dict):
            data = cast(DailyNoteData, data['data'])
        return data

    async def _mys_req_get(
        self,
        url: str,
        is_os: bool,
        params: Dict,
        header: Optional[Dict] = None,
    ) -> Union[Dict, int]:
        if is_os:
            _URL = _API[f'{url}_OS']
            HEADER = copy.deepcopy(self._HEADER_OS)
            use_proxy = True
        else:
            _URL = _API[url]
            HEADER = copy.deepcopy(self._HEADER)
            use_proxy = False
        if header:
            HEADER.update(header)

        if 'Cookie' not in HEADER and 'uid' in params:
            ck = await self.get_ck(params['uid'])
            if ck is None:
                return -51
            HEADER['Cookie'] = ck
        data = await self._mys_request(
            url=_URL,
            method='GET',
            header=HEADER,
            params=params,
            use_proxy=use_proxy,
        )
        return data

    async def simple_mys_req(
        self,
        URL: str,
        uid: Union[str, bool],
        params: Dict = {},
        header: Dict = {},
        cookie: Optional[str] = None,
    ) -> Union[Dict, int]:
        if isinstance(uid, bool):
            is_os = uid
            server_id = 'cn_qd01' if is_os else 'prod_gf_cn'
        else:
            server_id = RECOGNIZE_SERVER.get(uid[0])
            is_os = False if int(uid[0]) < 6 else True
        ex_params = '&'.join([f'{k}={v}' for k, v in params.items()])
        if is_os:
            _URL = _API[f'{URL}_OS']
            HEADER = copy.deepcopy(self._HEADER_OS)
            HEADER['DS'] = generate_os_ds()
        else:
            _URL = _API[URL]
            HEADER = copy.deepcopy(self._HEADER)
            HEADER['DS'] = get_ds_token(
                ex_params if ex_params else f'role_id={uid}&server={server_id}'
            )
        HEADER.update(header)
        if cookie is not None:
            HEADER['Cookie'] = cookie
        elif 'Cookie' not in HEADER and isinstance(uid, str):
            ck = await self.get_ck(uid)
            if ck is None:
                return -51
            HEADER['Cookie'] = ck
        data = await self._mys_request(
            url=_URL,
            method='GET',
            header=HEADER,
            params=params if params else {'server': server_id, 'role_id': uid},
            use_proxy=True if is_os else False,
        )
        return data


mys_api = _MysApi()
