"""Mihomo.me api 包装
"""
from .models import MihomoData as MihomoData
from .requests import get_char_card_info as get_char_card_info

__all__ = ["requests", "MihomoData"]
