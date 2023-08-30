import json
import os
from pathlib import Path
from typing import Dict

from httpx import AsyncClient


def get_all_file(path):
    # 获取文件夹下所有文件的路径
    file_list = []
    for root, _dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list


FILE_ROOT_MAP = [
    'character',
    'character_portrait',
    'character_preview',
    'consumable',
    'element',
    'light_cone',
    'relic',
    'skill',
]

WIKI_ROOT_MAP = [
    'lightcone',
    'material for role',
    'relic',
    'role',
]

GUIDE_ROOT_MAP = [
    'lightcone',
    'character'
]

input_path = Path("C:/Users/qwerdvd/Desktop/gsuid_core/data/StarRailUID/resource")
wiki_path = Path("C:/Users/qwerdvd/Desktop/gsuid_core/data/StarRailUID/wiki")
guide_path = Path("C:/Users/qwerdvd/Desktop/gsuid_core/data/StarRailUID/guide")
file_list = get_all_file(input_path)
wiki_file_list = get_all_file(wiki_path)
guide_file_list = get_all_file(guide_path)
file_map = {
    'resource': {
        'character': {},
        'character_portrait': {},
        'character_preview': {},
        'consumable': {},
        'element': {},
        'light_cone': {},
        'relic': {},
        'skill': {}
    },
    'wiki': {
        'lightcone': {},
        'material for role': {},
        'relic': {},
        'role': {},
    },
    'guide': {
        'lightcone': {},
        'character': {}
    }
}


async def upload(file_path: str, token: str) -> Dict:
    async with AsyncClient(
        timeout=10
    ) as client:
        req = await client.post(
            'http://182.43.43.40:8765/nor.php',
            data={
                'token': token
            },
            files={
                'file': open(file_path, 'rb')
            }
        )
        print(req.status_code)
        print(req.text)
        return req.json()


async def main(token: str):
    for file_root in FILE_ROOT_MAP:
        for file in file_list:
            file_name = file.split('\\')[-1]
            file_path = file.split('\\')[-2]
            if file_path == file_root:
                print(f'upload res {file_path}_{file_name}')
                data = await upload(file, token)
                image_info_array = data[0]['image_info_array']
                for image_info in image_info_array:
                    size = image_info['size']
                    url = image_info['url']
                    file_map['resource'][file_root][file_name] = {
                        'size': size,
                        'url': url
                    }
    for file_root in WIKI_ROOT_MAP:
        for file in wiki_file_list:
            file_name = file.split('\\')[-1]
            file_path = file.split('\\')[-2]
            if file_path == file_root:
                print(f'upload wiki {file_path}_{file_name}')
                data = await upload(file, token)
                image_info_array = data[0]['image_info_array']
                for image_info in image_info_array:
                    size = image_info['size']
                    url = image_info['url']
                    file_map['wiki'][file_root][file_name] = {
                        'size': size,
                        'url': url
                    }
    for file_root in GUIDE_ROOT_MAP:
        for file in guide_file_list:
            file_name = file.split('\\')[-1]
            file_path = file.split('\\')[-2]
            if file_path == file_root:
                print(f'upload guide {file_path}_{file_name}')
                data = await upload(file, token)
                image_info_array = data[0]['image_info_array']
                for image_info in image_info_array:
                    size = image_info['size']
                    url = image_info['url']
                    file_map['guide'][file_root][file_name] = {
                        'size': size,
                        'url': url
                    }
    with open('./file_map.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(file_map, ensure_ascii=False))
    print(json.dumps(file_map, ensure_ascii=False))


if __name__ == '__main__':
    import asyncio
    token = 'BtxqvjajYEtbpzG3OJ5giOX06QVCQYzC'
    asyncio.run(main(token))
