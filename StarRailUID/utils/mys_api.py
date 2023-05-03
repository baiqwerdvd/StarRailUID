import copy
import random
from typing import Dict, Union, cast
from string import digits, ascii_letters

from gsuid_core.utils.api.mys_api import _MysApi
from gsuid_core.utils.api.mys.models import MysSign, SignInfo, SignList
from gsuid_core.utils.api.mys.tools import (
    random_hex,
    generate_os_ds,
    get_web_ds_token,
)

from ..sruid_utils.api.mys.api import _API
from ..sruid_utils.api.mys.models import (
    RoleIndex,
    AvatarInfo,
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


class MysApi(_MysApi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    async def get_role_index(self, uid: str) -> Union[RoleIndex, int]:
        data = await self.simple_mys_req('STAR_RAIL_INDEX_URL', uid)
        if isinstance(data, Dict):
            data = cast(RoleIndex, data['data'])
        return data

    async def get_avatar_info(
        self, uid: str, avatar_id: int, need_wiki: bool = False
    ) -> Union[AvatarInfo, int]:
        data = await self.simple_mys_req(
            'STAR_RAIL_AVATAR_INFO_URL',
            uid,
            params={
                "id": avatar_id,
                "need_wiki": "true" if need_wiki else "false",
            },
        )
        if isinstance(data, Dict):
            data = cast(AvatarInfo, data['data'])
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


mys_api = MysApi()