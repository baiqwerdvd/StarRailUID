from typing import Dict, Union

from msgspec import Struct


class RelicSetStatusAdd(Struct):
    Property: str
    Value: float


class RelicSetSkillModel(Struct):
    RelicSet: Dict[str, Dict[str, Union[RelicSetStatusAdd, None]]]

    @classmethod
    def from_json(cls, data: Dict):
        return cls(RelicSet={
            str(k): {
                str(k2): RelicSetStatusAdd(
                    Property=v2['Property'],
                    Value=v2['Value']
                ) if v2 else None
                for k2, v2 in v.items()
            }
            for k, v in data.items()
        })
