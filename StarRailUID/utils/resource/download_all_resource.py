import asyncio

from .download_from_cos import download_all_file_from_cos


async def download_all_resource():
    ret = await asyncio.gather(download_all_file_from_cos())
    ret = [str(x) for x in ret if x]
    if ret:
        return '\n'.join(ret)
    return 'sr全部资源下载完成!'
