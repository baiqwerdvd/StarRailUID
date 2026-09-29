from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, Mock, patch

from msgspec import json as msgjson
from starrail_damage_cal.mihomo.models import Avatar, MihomoData, PlayerDetailInfo
from starrail_damage_cal.model import MihomoCharacter
from starrail_damage_cal.to_data import get_data

from tests.support import load_module, stub_module


class PanelCacheTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name)
        self.char, _ = await get_data(
            SimpleNamespace(
                avatarId=1001,
                promotion=0,
                level=20,
                skillTreeList=[],
                relicList=[],
                rank=0,
                equipment=None,
                enhancedId=0,
            ),
            "tester",
            "100000001",
        )
        self.stubs = {
            "gsuid_core.logger": stub_module("gsuid_core.logger", logger=Mock()),
            "StarRailUID.utils.error_reply": stub_module("error_reply", CHAR_HINT="{} {}"),
            "StarRailUID.utils.resource.RESOURCE_PATH": stub_module("RESOURCE_PATH", PLAYER_PATH=self.path),
            "StarRailUID.utils.name_covert": stub_module(
                "name_covert",
                name_to_avatar_id=AsyncMock(return_value="1001"),
                alias_to_char_name=AsyncMock(),
                alias_to_weapon_name=AsyncMock(),
                name_to_weapon_id=AsyncMock(),
            ),
            "StarRailUID.starrailuid_charinfo.draw_char_img": stub_module(
                "draw_char_img", draw_char_img=AsyncMock()
            ),
        }
        self.query = load_module("StarRailUID/starrailuid_charinfo/get_char_img.py", self.stubs)

    def write_character(self, source=None, self_cache=False):
        folder = self.path / self.char.uid
        if self_cache:
            folder /= "SELF"
        folder.mkdir(parents=True, exist_ok=True)
        data = msgjson.decode(msgjson.encode(self.char))
        data.pop("source", None)
        data.pop("updated_at", None)
        if source:
            data.update(source=source, updated_at="2026-09-20T01:02:03+00:00")
        path = folder / f"{self.char.avatarName}.json"
        path.write_bytes(msgjson.encode(data))
        return path

    async def test_cached_source_is_per_character_and_legacy_is_unknown(self):
        for stored, expected in [("mys", "mys"), ("mihomo", "mihomo"), (None, "cache")]:
            with self.subTest(source=stored):
                path = self.write_character(stored)
                before = path.read_bytes()
                char, source = await self.query.get_char_data_with_source(
                    self.char.uid, self.char.avatarName
                )
                self.assertEqual(source, expected)
                self.assertEqual(char.avatarId, 1001)
                self.assertEqual(path.read_bytes(), before)

    async def test_self_cache_is_labeled_simulated(self):
        self.write_character("mys", self_cache=True)
        _, source = await self.query.get_char_data_with_source(self.char.uid, self.char.avatarName)
        self.assertEqual(source, "self")

    async def test_rank_override_is_labeled_simulated(self):
        self.write_character("mys")
        args = await self.query.get_char_args(f"零魂{self.char.avatarName}", self.char.uid)
        self.assertEqual(args[-1], "simulated")

    async def test_footer_uses_stored_time_and_never_invents_old_cache_time(self):
        cache = load_module("StarRailUID/starrailuid_charinfo/panel_cache.py", self.stubs)
        path = self.write_character("mys")
        char = msgjson.decode(path.read_bytes(), type=MihomoCharacter)
        self.assertEqual(cache.panel_updated_at(char, char.uid, "mys"), "2026-09-20 01:02:03 UTC")
        self.assertIn("MiYouShe", cache.panel_watermark("mys"))
        self.assertEqual(cache.panel_updated_at(char, char.uid, "simulated"), "")
        self.assertIn("Simulated", cache.panel_watermark("simulated"))
        path = self.write_character()
        old = msgjson.decode(path.read_bytes(), type=MihomoCharacter)
        self.assertEqual(cache.panel_updated_at(old, old.uid, "cache"), "")
        self.assertIn("source unknown", cache.panel_watermark("cache"))

    async def test_refresh_persists_source_and_time_with_installed_dependency(self):
        mys_avatar = SimpleNamespace(
            id=1302,
            level=20,
            promotion=0,
            cur_enhanced_id=0,
            skills=[],
            relics=[],
            ornaments=[],
            ranks=[],
            equip=None,
        )
        raw = MihomoData(
            detailInfo=PlayerDetailInfo(
                isDisplayAvatar=True,
                uid=100000001,
                nickname="tester",
                level=70,
                avatarDetailList=[Avatar(avatarId=1001, level=20, skillTreeList=[])],
            )
        )
        for source, name in [("mys", "银枝"), ("mihomo", "三月七")]:
            with self.subTest(source=source):
                stubs = dict(self.stubs)
                stubs.update(
                    {
                        "StarRailUID.starrailuid_config.sr_config": stub_module(
                            "sr_config",
                            get_panel_source=lambda value=source: value,
                        ),
                        "StarRailUID.utils.mys_api": stub_module(
                            "mys_api",
                            mys_api=SimpleNamespace(
                                get_avatar_panel_info=AsyncMock(
                                    return_value=("tester", SimpleNamespace(avatar_list=[mys_avatar]))
                                ),
                            ),
                        ),
                    }
                )
                panel = load_module("StarRailUID/starrailuid_charinfo/panel_data.py", stubs)
                panel.get_char_card_info = AsyncMock(return_value=raw)
                with patch.dict("sys.modules", {"StarRailUID.starrailuid_charinfo.panel_data": panel}):
                    _, loaded_source = await self.query.get_char_data_with_source(self.char.uid, name)
                self.assertEqual(loaded_source, source)
                path = self.path / self.char.uid / f"{name}.json"
                data = msgjson.decode(path.read_bytes())
                self.assertEqual(data.get("source"), source)
                self.assertTrue(data.get("updated_at"))
                before = path.read_bytes()
                _, loaded_source = await self.query.get_char_data_with_source(self.char.uid, name)
                self.assertEqual(loaded_source, source)
                self.assertEqual(path.read_bytes(), before)
