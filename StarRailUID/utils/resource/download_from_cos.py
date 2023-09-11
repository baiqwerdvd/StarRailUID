import asyncio
from pathlib import Path
from typing import Dict, List, Tuple, Union

from aiohttp.client import ClientSession
from msgspec import json as msgjson

from gsuid_core.logger import logger

from .download_url import download_file
from .RESOURCE_PATH import GUIDE_PATH, RESOURCE_PATH, WIKI_PATH

with Path.open(
    Path(__file__).parent / 'resource_map.json', encoding='UTF-8'
) as f:
    resource_map = msgjson.decode(
        f.read(),
        type=Dict[str, Dict[str, Dict[str, Dict[str, Union[str, int]]]]],
    )


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
                    'lightcone',
                    'material for role',
                    'relic',
                    'role',
                ]
            else:
                logger.info('[cos]开始下载guide文件...')
                resource_type_list = [
                    'lightcone',
                    'character',
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
                                timeout=60,
                            )
                        )
                        # await download_file(url, FILE_TO_PATH[file], name)
                        if len(TASKS) >= 10:
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
                    timeout=60,
                )
            )
            if len(TASKS) >= 10:
                await _download(TASKS)
        await _download(TASKS)
        if count := len(failed_list):
            logger.error(
                f'[cos]仍有{count}个文件未下载,请使用命令 `下载全部资源` 重新下载'
            )
