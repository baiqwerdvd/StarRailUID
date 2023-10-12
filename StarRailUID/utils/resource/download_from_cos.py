import asyncio
from pathlib import Path
from typing import Dict, List, Tuple, Union

from aiohttp import ClientTimeout, TCPConnector
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup
from gsuid_core.logger import logger
from gsuid_core.utils.download_resource.download_core import check_url
from gsuid_core.utils.download_resource.download_file import download
from msgspec import json as msgjson

from .download_url import download_file
from .RESOURCE_PATH import (
    CHAR_ICON_PATH,
    CHAR_PORTRAIT_PATH,
    CHAR_PREVIEW_PATH,
    CONSUMABLE_PATH,
    ELEMENT_PATH,
    GUIDE_CHARACTER_PATH,
    GUIDE_LIGHT_CONE_PATH,
    GUIDE_PATH,
    RELIC_PATH,
    RESOURCE_PATH,
    SKILL_PATH,
    WEAPON_PATH,
    WIKI_LIGHT_CONE_PATH,
    WIKI_MATERIAL_FOR_ROLE,
    WIKI_PATH,
    WIKI_RELIC_PATH,
    WIKI_ROLE_PATH,
)

with Path.open(
    Path(__file__).parent / 'resource_map.json', encoding='UTF-8'
) as f:
    resource_map = msgjson.decode(
        f.read(),
        type=Dict[str, Dict[str, Dict[str, Dict[str, Union[str, int]]]]],
    )


async def find_fastest_url(urls: Dict[str, str]):
    tasks = []
    for tag in urls:
        tasks.append(asyncio.create_task(check_url(tag, urls[tag])))

    results: list[tuple[str, str, float]] = await asyncio.gather(
        *tasks, return_exceptions=True
    )
    fastest_tag = ''
    fastest_url = None
    fastest_time = float('inf')

    for result in results:
        if isinstance(result, Exception):
            continue
        tag, url, elapsed_time = result
        if elapsed_time < fastest_time:
            fastest_url = url
            fastest_time = elapsed_time
            fastest_tag = tag

    return fastest_tag, fastest_url


async def check_speed():
    logger.info('[GsCore资源下载]测速中...')

    URL_LIB = {
        '[qxqx]': 'https://kr-arm.qxqx.me',
        '[cos]': 'http://182.43.43.40:8765',
    }

    TAG, BASE_URL = await find_fastest_url(URL_LIB)
    logger.info(f'最快资源站: {TAG} {BASE_URL}')
    return TAG, BASE_URL


async def check_use():
    tag, _ = await check_speed()
    logger.info(tag, _)
    if tag == '[qxqx]':
        await download_all_file(
            'https://kr-arm.qxqx.me',
            '[qxqx]',
            'StarRailUID',
            {
                'resource/character': CHAR_ICON_PATH,
                'resource/character_portrait': CHAR_PORTRAIT_PATH,
                'resource/character_preview': CHAR_PREVIEW_PATH,
                'resource/consumable': CONSUMABLE_PATH,
                'resource/element': ELEMENT_PATH,
                'guide/character_overview': GUIDE_CHARACTER_PATH,
                'guide/light_cone': GUIDE_LIGHT_CONE_PATH,
                'resource/relic': RELIC_PATH,
                'resource/skill': SKILL_PATH,
                'resource/light_cone': WEAPON_PATH,
                'wiki/light_cone': WIKI_LIGHT_CONE_PATH,
                'wiki/character_material': WIKI_MATERIAL_FOR_ROLE,
                'wiki/relic_set': WIKI_RELIC_PATH,
                'wiki/character_overview': WIKI_ROLE_PATH,
            },
        )
    if tag == '[cos]':
        await download_all_file_from_cos()
    return 'sr全部资源下载完成!'


async def download_all_file_from_cos():
    async def _download(tasks: List[asyncio.Task]):
        failed_list.extend(
            list(filter(lambda x: x is not None, await asyncio.gather(*tasks)))
        )
        tasks.clear()
        logger.info('[cos]下载完成!')

    failed_list: List[Tuple[str, str, str, str]] = []
    TASKS = []
    async with ClientSession() as sess:
        for res_type in ['resource', 'wiki', 'guide']:
            if res_type == 'resource':
                logger.info('[cos]开始下载资源文件...')
                resource_type_list = [
                    'character',
                    'character_portrait',
                    'character_preview',
                    'consumable',
                    'element',
                    'light_cone',
                    'relic',
                    'skill',
                ]
            elif res_type == 'wiki':
                logger.info('[cos]开始下载wiki文件...')
                resource_type_list = [
                    'light_cone',
                    'character_material',
                    'relic_set',
                    'character_overview',
                ]
            else:
                logger.info('[cos]开始下载guide文件...')
                resource_type_list = [
                    'light_cone',
                    'character_overview',
                ]
            for resource_type in resource_type_list:
                file_dict = resource_map[res_type][resource_type]
                logger.info(
                    f'[cos]数据库[{resource_type}]中存在{len(file_dict)}个内容!'
                )
                temp_num = 0
                for file_name, file_info in file_dict.items():
                    name = file_name
                    size = file_info['size']
                    url = file_info['url']
                    if res_type == 'resource':
                        path = Path(RESOURCE_PATH / resource_type / name)
                    elif res_type == 'wiki':
                        path = Path(WIKI_PATH / resource_type / name)
                    else:
                        path = Path(GUIDE_PATH / resource_type / name)
                    if path.exists():
                        is_diff = size == Path.stat(path).st_size
                    else:
                        is_diff = True
                    if (
                        not path.exists()
                        or not Path.stat(path).st_size
                        or not is_diff
                    ):
                        logger.info(f'[cos]开始下载[{resource_type}]_[{name}]...')
                        temp_num += 1
                        if isinstance(url, int):
                            logger.error(
                                f'[cos]数据库[{resource_type}]_[{name}]下载失败!'
                            )
                            continue
                        TASKS.append(
                            asyncio.wait_for(
                                download_file(
                                    url, res_type, resource_type, name, sess
                                ),
                                timeout=600,
                            )
                        )
                        # await download_file(url, FILE_TO_PATH[file], name)
                        if len(TASKS) >= 5:
                            await _download(TASKS)
                await _download(TASKS)
                if temp_num == 0:
                    im = f'[cos]数据库[{resource_type}]无需下载!'
                else:
                    im = f'[cos]数据库[{resource_type}]已下载{temp_num}个内容!'
                temp_num = 0
                logger.info(im)
    if failed_list:
        logger.info(f'[cos]开始重新下载失败的{len(failed_list)}个文件...')
        for url, res_type, resource_type, name in failed_list:
            TASKS.append(
                asyncio.wait_for(
                    download_file(url, res_type, resource_type, name, sess),
                    timeout=600,
                )
            )
            if len(TASKS) >= 5:
                await _download(TASKS)
        await _download(TASKS)
        if count := len(failed_list):
            logger.error(f'[cos]仍有{count}个文件未下载,请使用命令 `下载全部资源` 重新下载')


async def _get_url(url: str, sess: ClientSession):
    req = await sess.get(url=url)
    return await req.read()


async def download_all_file(
    BASE_URL: str, TAG: str, plugin_name: str, EPATH_MAP: Dict[str, Path]
):
    PLUGIN_RES = f'{BASE_URL}/{plugin_name}'
    logger.info(PLUGIN_RES)

    TASKS = []
    async with ClientSession(
        connector=TCPConnector(verify_ssl=False),
        timeout=ClientTimeout(total=None, sock_connect=20, sock_read=200),
    ) as sess:
        for endpoint in EPATH_MAP:
            url = f'{PLUGIN_RES}/{endpoint}/'
            path = EPATH_MAP[endpoint]

            base_data = await _get_url(url, sess)
            content_bs = BeautifulSoup(base_data, 'lxml')
            pre_data = content_bs.find_all('pre')[0]
            data_list = pre_data.find_all('a')
            size_list = list(content_bs.strings)
            logger.info(f'{TAG} 数据库 {endpoint} 中存在 {len(data_list)} 个内容!')

            temp_num = 0
            for index, data in enumerate(data_list):
                if data['href'] == '../':
                    continue
                file_url = f'{url}{data["href"]}'
                name: str = data.text
                size = size_list[index * 2 + 6].split(' ')[-1]
                size = size.replace('\r\n', '')
                file_path = path / name
                if file_path.exists():
                    is_diff = size == str(Path.stat(file_path).st_size)
                else:
                    is_diff = True
                if (
                    not file_path.exists()
                    or not Path.stat(file_path).st_size
                    or not is_diff
                ):
                    logger.info(
                        f'{TAG} {plugin_name} 开始下载 {endpoint}/{name} ...'
                    )
                    temp_num += 1
                    TASKS.append(
                        asyncio.wait_for(
                            download(file_url, path, name, sess, TAG),
                            timeout=600,
                        )
                    )
                    if len(TASKS) >= 10:
                        await asyncio.gather(*TASKS)
                        TASKS.clear()
            await asyncio.gather(*TASKS)
            TASKS.clear()

            if temp_num == 0:
                im = f'{TAG} 数据库 {endpoint} 无需下载!'
            else:
                im = f'{TAG}数据库 {endpoint} 已下载{temp_num}个内容!'
            temp_num = 0
            logger.info(im)
