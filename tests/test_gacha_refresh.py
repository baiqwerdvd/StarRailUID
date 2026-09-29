import asyncio
from contextlib import asynccontextmanager
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, Mock, patch

from tests.support import ROOT, load_module, stub_module


@asynccontextmanager
async def async_open(path, mode="r", encoding="UTF-8"):
    with Path(path).open(mode, encoding=encoding) as file:  # noqa: ASYNC230
        yield SimpleNamespace(
            read=AsyncMock(side_effect=file.read),
            write=AsyncMock(side_effect=file.write),
        )


def raw_record(record_id="1700000000001", count=75):
    return {
        "id": record_id,
        "uuid": "test",
        "item": {
            "item_id": 1001,
            "name": "测试角色",
            "icon": "",
            "big_icon": "",
            "item_type": "Avatar",
            "rarity": 5,
        },
        "is_up": True,
        "got_item": True,
        "gacha_count": count,
    }


def response(records=(), has_more=False, next_id=None):
    return {
        "retcode": 0,
        "data": {
            "list": list(records),
            "has_more": has_more,
            "next_max_id": next_id,
            "version_id": "1",
        },
    }


class RefreshTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.path = self.root / "100" / "gacha_logs_wx.json"
        self.path.parent.mkdir()
        self.api = SimpleNamespace(
            login_gacha_account=AsyncMock(return_value="cookie"),
            get_gacha_five_star_list=AsyncMock(return_value=response()),
        )
        stubs = {
            "aiofiles": stub_module("aiofiles", open=async_open),
            "gsuid_core.bot": stub_module("gsuid_core.bot", Bot=object),
            "gsuid_core.models": stub_module("gsuid_core.models", Event=object),
            "gsuid_core.logger": stub_module("gsuid_core.logger", logger=Mock()),
            "gsuid_core.utils.database.models": stub_module(
                "gsuid_core.utils.database.models",
                GsUser=SimpleNamespace(
                    base_select_data=AsyncMock(
                        return_value=SimpleNamespace(cookie="cookie", device_id="device")
                    )
                ),
            ),
            "StarRailUID.utils.mys_api": stub_module("StarRailUID.utils.mys_api", mys_api=self.api),
            "StarRailUID.utils.resource.RESOURCE_PATH": stub_module(
                "StarRailUID.utils.resource.RESOURCE_PATH", PLAYER_PATH=self.root
            ),
        }
        storage_path = "StarRailUID/starrailuid_gachalog/storage.py"
        if (ROOT / storage_path).exists():
            self.storage = load_module(storage_path)
            stubs["StarRailUID.starrailuid_gachalog.storage"] = self.storage
        self.official = load_module("StarRailUID/starrailuid_gachalog/get_gachalogs_new.py", stubs)
        self.legacy = load_module("StarRailUID/starrailuid_gachalog/get_gachalogs.py", stubs)
        self.official.asyncio = SimpleNamespace(sleep=AsyncMock())
        self.legacy.asyncio = SimpleNamespace(sleep=AsyncMock())
        self.event = SimpleNamespace(user_id="user", bot_id="bot")
        self.old = {
            "uid": "100",
            "data_time": "old",
            "data": {name: [] for name in self.official.POOL_MAP},
            "pity_counts": {"角色跃迁": 63},
        }
        self.old["data"]["角色跃迁"] = [
            {
                "uid": "100",
                "gacha_id": "",
                "gacha_type": "11",
                "item_id": "1001",
                "count": "1",
                "time": "2023-07-22 12:00:00",
                "name": "测试角色",
                "lang": "zh-cn",
                "item_type": "角色",
                "rank_type": "5",
                "id": "1690000000001",
                "gacha_count": 80,
                "is_up": True,
            }
        ]
        self.path.write_text(json.dumps(self.old), encoding="utf-8")

    async def refresh(self, **kwargs):
        return await self.official.save_gachalogs_new("100", None, self.event, **kwargs)

    async def test_failed_pool_preserves_history_and_pity_with_partial_status(self):
        async def fetch(**kwargs):
            if kwargs["gacha_type"] == "GachaType_AvatarUp":
                return {"retcode": -1}
            return response()

        self.api.get_gacha_five_star_list.side_effect = fetch
        message = await self.refresh()
        saved = json.loads(self.path.read_text())
        self.assertEqual(saved["data"]["角色跃迁"], self.old["data"]["角色跃迁"])
        self.assertEqual(saved["pity_counts"]["角色跃迁"], 63)
        self.assertEqual(saved["pool_data_time"]["角色跃迁"], "old")
        self.assertNotEqual(saved["pool_data_time"]["群星跃迁"], "old")
        self.assertIn("部分", message)
        self.assertIn("角色跃迁", message)
        self.assertNotIn("更新成功", message)

    async def test_failed_second_page_does_not_save_first_page(self):
        async def fetch(**kwargs):
            if kwargs["gacha_type"] != "GachaType_AvatarUp":
                return response()
            if kwargs["max_id"] is None:
                return response([raw_record()], True, "next")
            return {"retcode": -1}

        self.api.get_gacha_five_star_list.side_effect = fetch
        await self.refresh()
        saved = json.loads(self.path.read_text())
        self.assertEqual(saved["data"]["角色跃迁"], self.old["data"]["角色跃迁"])
        self.assertEqual(saved["pity_counts"]["角色跃迁"], 63)

    async def test_all_failed_leaves_file_unchanged(self):
        before = self.path.read_bytes()
        self.api.get_gacha_five_star_list.return_value = -1
        message = await self.refresh()
        self.assertEqual(self.path.read_bytes(), before)
        self.assertIn("失败", message)

    async def test_transport_failure_retains_pool_timestamp_and_pity(self):
        self.old["pool_data_time"] = {"角色跃迁": "older pool"}
        self.path.write_text(json.dumps(self.old))

        async def fetch(**kwargs):
            if kwargs["gacha_type"] == "GachaType_AvatarUp":
                raise TimeoutError("API timeout")
            return response()

        self.api.get_gacha_five_star_list.side_effect = fetch
        message = await self.refresh()
        saved = json.loads(self.path.read_text())
        self.assertEqual(saved["data"]["角色跃迁"], self.old["data"]["角色跃迁"])
        self.assertEqual(saved["pity_counts"]["角色跃迁"], 63)
        self.assertEqual(saved["pool_data_time"]["角色跃迁"], "older pool")
        self.assertIn("部分", message)

    async def test_missing_pagination_cursor_preserves_old_pool(self):
        async def fetch(**kwargs):
            if kwargs["gacha_type"] == "GachaType_AvatarUp":
                return response([raw_record()], has_more=True)
            return response()

        self.api.get_gacha_five_star_list.side_effect = fetch
        message = await self.refresh()
        saved = json.loads(self.path.read_text())
        self.assertEqual(saved["data"]["角色跃迁"], self.old["data"]["角色跃迁"])
        self.assertEqual(saved["pity_counts"]["角色跃迁"], 63)
        self.assertIn("失败", message)

    async def test_valid_empty_pool_updates_pity_to_zero(self):
        message = await self.refresh()
        saved = json.loads(self.path.read_text())
        self.assertEqual(saved["pity_counts"]["角色跃迁"], 0)
        self.assertEqual(saved["data"]["角色跃迁"], self.old["data"]["角色跃迁"])
        self.assertNotIn("失败", message)

    async def test_nonempty_pool_missing_pity_preserves_history_and_timestamp(self):
        for record_id in ("1700000000001", "1690000000001"):
            with self.subTest(record_id=record_id):
                self.path.write_text(json.dumps(self.old))

                async def fetch(record_id=record_id, **kwargs):
                    if kwargs["gacha_type"] == "GachaType_AvatarUp":
                        return response([raw_record(record_id)])
                    return response()

                self.api.get_gacha_five_star_list.side_effect = fetch
                message = await self.refresh()
                saved = json.loads(self.path.read_text())
                self.assertEqual(saved["data"]["角色跃迁"], self.old["data"]["角色跃迁"])
                self.assertEqual(saved["pity_counts"]["角色跃迁"], 63)
                self.assertEqual(saved["pool_data_time"]["角色跃迁"], "old")
                self.assertIn("部分", message)

    async def test_pity_after_existing_record_is_read_including_explicit_zero(self):
        for pity_count in (12, 0):
            with self.subTest(pity_count=pity_count):
                self.path.write_text(json.dumps(self.old))

                async def fetch(pity_count=pity_count, **kwargs):
                    if kwargs["gacha_type"] == "GachaType_AvatarUp":
                        pity = dict(raw_record("0", pity_count), item=None)
                        return response([raw_record(), raw_record("1690000000001"), pity])
                    return response()

                self.api.get_gacha_five_star_list.side_effect = fetch
                message = await self.refresh()
                saved = json.loads(self.path.read_text())
                self.assertEqual(saved["pity_counts"]["角色跃迁"], pity_count)
                self.assertEqual(saved["char_gacha_num"], 2)
                self.assertNotEqual(saved["pool_data_time"]["角色跃迁"], "old")
                self.assertNotIn("失败", message)

    async def test_success_merges_without_duplicate_ids(self):
        async def fetch(**kwargs):
            if kwargs["gacha_type"] == "GachaType_AvatarUp":
                pity = dict(raw_record("0", 12), item=None)
                return response([pity, raw_record(), raw_record("1690000000001")])
            return response()

        self.api.get_gacha_five_star_list.side_effect = fetch
        message = await self.refresh(is_force=True)
        saved = json.loads(self.path.read_text())
        self.assertEqual(
            [record["id"] for record in saved["data"]["角色跃迁"]],
            ["1700000000001", "1690000000001"],
        )
        self.assertEqual(saved["pity_counts"]["角色跃迁"], 12)
        self.assertEqual(saved["char_gacha_num"], 2)
        self.assertIn("新增五星记录 1 条", message)

    async def test_corrupt_history_is_not_overwritten(self):
        for content in ("{broken", '{"data": []}', '{"data": {"角色跃迁": {}}}'):
            with self.subTest(content=content):
                self.path.write_text(content)
                message = await self.refresh()
                self.assertEqual(self.path.read_text(), content)
                self.assertIn("失败", message)

    async def test_official_and_legacy_refresh_share_uid_serialization(self):
        started = asyncio.Event()
        release = asyncio.Event()

        async def fetch(**kwargs):
            started.set()
            await release.wait()
            return response()

        self.api.get_gacha_five_star_list.side_effect = fetch
        official = asyncio.create_task(self.refresh())
        await started.wait()
        legacy = asyncio.create_task(
            self.legacy.save_gachalogs("100", "", {name: [] for name in self.official.POOL_MAP})
        )
        try:
            await asyncio.sleep(0)
            self.assertFalse(legacy.done(), "legacy refresh must wait for official refresh")
        finally:
            release.set()
            await asyncio.gather(official, legacy)

    async def test_atomic_replace_failure_keeps_previous_file(self):
        before = self.path.read_bytes()
        with patch("os.replace", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                await self.refresh()
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    async def test_legacy_atomic_replace_failure_keeps_previous_file(self):
        legacy_path = self.path.with_name("gacha_logs.json")
        content = json.dumps({"data": {name: [] for name in self.official.POOL_MAP}})
        legacy_path.write_text(content)
        with patch("os.replace", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                await self.legacy.save_gachalogs("100", "", {name: [] for name in self.official.POOL_MAP})
        self.assertEqual(legacy_path.read_text(), content)
        self.assertEqual(set(self.path.parent.iterdir()), {self.path, legacy_path})


if __name__ == "__main__":
    unittest.main()
