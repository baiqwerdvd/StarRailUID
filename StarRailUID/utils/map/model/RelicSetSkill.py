from msgspec import Struct


class RelicSetStatusAdd(Struct):
    Property: str
    Value: float
