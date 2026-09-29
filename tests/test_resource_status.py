# ruff: noqa: RUF001
import asyncio
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, Mock, patch

from PIL import Image

from tests.support import load_module, stub_module


class ResourceStatusTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = self.root / "runtime"
        self.data.mkdir()
        self.images = self.root / "images"
        self.images.mkdir()
        self.paths = stub_module(
            "starrail_damage_cal.data_paths",
            resolve_data_path=lambda name: self.data / name,
            resolve_version_file=lambda: self.data / "version.json",
            runtime_path=lambda name: self.data / name,
        )
        self.updater = stub_module(
            "starrail_damage_cal.update",
            managed_relative_path=lambda name: Path("map/data") / name,
            calc_sha256=lambda path: hashlib.sha256(path.read_bytes()).hexdigest(),
            SKIPPED_FILES={"light_cone_ranks.json"},
            update_resource=AsyncMock(return_value="数据文件已是最新"),
            refresh_loaded_data=Mock(),
        )
        service = Mock()
        service.on_fullmatch.side_effect = lambda *_: lambda function: function
        self.download = AsyncMock(return_value="sr全部资源下载完成!")
        self.ranks = AsyncMock(return_value="光锥评价数据已是最新版本")
        self.stubs = {
            "starrail_damage_cal": stub_module(
                "starrail_damage_cal", data_paths=self.paths, update=self.updater
            ),
            "starrail_damage_cal.data_paths": self.paths,
            "starrail_damage_cal.update": self.updater,
            "starrail_damage_cal.excel.model": stub_module("starrail_damage_cal.excel.model"),
            "starrail_damage_cal.map.SR_MAP_PATH": stub_module("starrail_damage_cal.map.SR_MAP_PATH"),
            "gsuid_core.bot": stub_module("gsuid_core.bot", Bot=object),
            "gsuid_core.models": stub_module("gsuid_core.models", Event=object),
            "gsuid_core.logger": stub_module("gsuid_core.logger", logger=Mock()),
            "gsuid_core.sv": stub_module("gsuid_core.sv", SV=Mock(return_value=service)),
            "StarRailUID.utils.excel.read_excel": stub_module(
                "StarRailUID.utils.excel.read_excel", update_light_cone_ranks=self.ranks
            ),
            "StarRailUID.utils.resource.download_all_file": stub_module(
                "StarRailUID.utils.resource.download_all_file", check_use=self.download
            ),
            "StarRailUID.utils.resource.RESOURCE_PATH": stub_module(
                "StarRailUID.utils.resource.RESOURCE_PATH",
                MAIN_PATH=self.root,
                CHAR_ICON_PATH=self.images / "character",
                WEAPON_PATH=self.images / "light_cone",
            ),
        }
        self.module = self.load()

    def load(self):
        self.stubs["StarRailUID.starrailuid_resource.resource_status"] = load_module(
            "StarRailUID/starrailuid_resource/resource_status.py", self.stubs
        )
        return load_module("StarRailUID/starrailuid_resource/__init__.py", self.stubs)

    def write_data(self):
        files = {}
        for name, value in (
            ("avatarId2Name_mapping.json", {"1001": "角色甲", "1002": "角色乙"}),
            ("EquipmentID2Name_mapping.json", {"20001": "光锥甲"}),
        ):
            path = self.data / "map/data" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value), encoding="utf-8")
            files[name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        (self.data / "version.json").write_text(
            json.dumps({"version": "9.8.7", "file_names": list(files), "files": files}),
            encoding="utf-8",
        )
        icon = self.images / "character/1001.png"
        icon.parent.mkdir(parents=True)
        Image.new("RGB", (2, 2)).save(icon)
        corrupt = self.images / "light_cone/20001.png"
        corrupt.parent.mkdir(parents=True)
        corrupt.write_bytes(b"broken png")

    async def test_status_is_read_only_and_counts_required_images(self):
        self.write_data()
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        bot = Mock(send=AsyncMock())
        with patch("socket.socket.connect", side_effect=AssertionError("network forbidden")):
            await self.module.send_resource_status(bot, object())
        result = bot.send.call_args.args[0]
        self.assertIn("9.8.7", result)
        self.assertIn("尚未检查", result)
        self.assertIn("角色图标: 共 2，缺失 1，损坏 0", result)
        self.assertIn("光锥图标: 共 1，缺失 0，损坏 1", result)
        self.assertIn("数据校验: 共 2，异常 0", result)
        self.assertNotIn(str(self.root), result)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.download.assert_not_awaited()
        self.updater.update_resource.assert_not_awaited()

    async def test_missing_and_malformed_manifest_never_report_healthy(self):
        manifest = self.data / "version.json"
        for content in (
            None,
            "{",
            "[]",
            "{}",
            json.dumps({"version": "9.8.7", "files": {}, "file_names": ["light_cone_ranks.json"]}),
        ):
            with self.subTest(content=content):
                if content is not None:
                    manifest.write_text(content, encoding="utf-8")
                result = self.module.get_resource_status()
                self.assertIn("数据校验: 未检查", result)
                self.assertIn("运行数据版本: 未知", result)
                self.assertTrue(self.module._get_invalid_data_files())  # noqa: SLF001

    async def test_corrupt_data_uses_hash_and_unreadable_map_is_not_empty_success(self):
        self.write_data()
        (self.data / "map/data/avatarId2Name_mapping.json").write_text("{", encoding="utf-8")
        result = self.module.get_resource_status()
        self.assertIn("数据校验: 共 2，异常 1", result)
        self.assertIn("角色图标: 未检查", result)

    async def test_locked_status_does_not_inspect_partial_files(self):
        async with self.module._RESOURCE_SYNC_LOCK:  # noqa: SLF001
            result = self.module.get_resource_status()
        self.assertIn("更新中", result)
        self.assertNotIn("异常 0", result)

    async def test_failed_stage_is_persisted_and_survives_module_reload(self):
        self.write_data()
        self.ranks.return_value = "光锥评价数据校验失败"
        await self.module.sync_all_resources(silent=True)
        result = self.load().get_resource_status()
        self.assertIn("失败", result)
        self.assertIn("光锥评价", result)
        self.assertRegex(result, r"\d{4}-\d{2}-\d{2}T")
        self.assertNotIn(str(self.root), result)

    async def test_reload_failure_is_not_recorded_as_success(self):
        self.write_data()
        self.updater.refresh_loaded_data.side_effect = RuntimeError("private path")
        await self.module.sync_all_resources(silent=True)
        result = self.load().get_resource_status()
        self.assertIn("失败", result)
        self.assertIn("数据刷新", result)
        self.assertNotIn("private path", result)

    async def test_successful_sync_and_interrupted_sync_are_distinct(self):
        self.write_data()
        await self.module.sync_all_resources(silent=True)
        self.assertIn("成功", self.load().get_resource_status())
        self.download.side_effect = asyncio.CancelledError()
        with self.assertRaises(asyncio.CancelledError):
            await self.module.sync_all_resources(silent=True)
        self.assertIn("中断", self.load().get_resource_status())
