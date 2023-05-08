from pathlib import Path
from typing import Dict, TypedDict

from msgspec import json as msgjson

from ...version import StarRail_version

MAP = Path(__file__).parent / 'data'

version = StarRail_version

avatarId2Name_fileName = f'avatarId2Name_mapping_{version}.json'
EquipmentID2Name_fileName = f'EquipmentID2Name_mapping_{version}.json'


class TS(TypedDict):
    Name: Dict[str, str]
    Icon: Dict[str, str]


with open(MAP / avatarId2Name_fileName, 'r', encoding='UTF-8') as f:
    avatarId2Name = msgjson.decode(f.read(), type=Dict[str, str])

with open(MAP / EquipmentID2Name_fileName, 'r', encoding='UTF-8') as f:
    EquipmentID2Name = msgjson.decode(f.read(), type=Dict[str, str])
