import copy
from datetime import datetime, timedelta
import unittest

from tests.support import load_module


def legacy_history(total=100, five_at=80):
    records = []
    for index in range(total):
        records.append(
            {
                "id": str(1000000000000 + index),
                "name": "姬子" if index + 1 == five_at else "三星光锥",
                "item_type": "角色" if index + 1 == five_at else "光锥",
                "rank_type": "5" if index + 1 == five_at else "3",
                "time": (datetime(2026, 1, 1) + timedelta(minutes=index)).strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    return {
        "data_time": "2026-01-01 02-00-00",
        "char_gacha_num": total,
        "data": {"角色跃迁": list(reversed(records))},
    }


def official_record(count=70, name="希儿", record_id="2000000000000", time="2026-02-01 12:00:00"):
    return {
        "id": record_id,
        "name": name,
        "item_type": "角色",
        "rank_type": "5",
        "time": time,
        "gacha_count": count,
        "is_up": True,
    }


def official_history(records, pity=5, updated="2026-02-01 13:00:00"):
    return {"data_time": updated, "data": {"角色跃迁": records}, "pity_counts": {"角色跃迁": pity}}


class GachaStatsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stats = load_module("StarRailUID/starrailuid_gachalog/gacha_stats.py")

    def test_mixed_history_replaces_old_pity_when_new_five_arrives(self):
        old = legacy_history()
        new = official_history([official_record()])
        before = copy.deepcopy((old, new))
        pools, counts = self.stats.build_gacha_statistics(old, new)
        self.assertEqual(counts["角色跃迁"], 155)
        self.assertEqual(pools["角色跃迁"]["remain"], 5)
        self.assertEqual(pools["角色跃迁"]["total"], 2)
        self.assertEqual((old, new), before, "Rendering must not mutate loaded records")

    def test_shared_five_uses_official_interval_and_up_flag_once(self):
        old = legacy_history()
        shared = next(x for x in old["data"]["角色跃迁"] if x["rank_type"] == "5")
        new = official_history([official_record(80, "姬子", shared["id"], shared["time"])], pity=25)
        pools, counts = self.stats.build_gacha_statistics(old, new)
        self.assertEqual(counts["角色跃迁"], 105)
        self.assertEqual(pools["角色跃迁"]["total"], 1)
        self.assertTrue(pools["角色跃迁"]["list"][0]["is_up"])

    def test_backfilled_history_is_sorted_and_recovers_full_first_interval(self):
        old = legacy_history(25, 5)
        first = next(x for x in old["data"]["角色跃迁"] if x["rank_type"] == "5")
        shared = official_record(80, "姬子", first["id"], first["time"])
        earlier = official_record(60, time="2025-12-01 12:00:00")
        pools, counts = self.stats.build_gacha_statistics(old, official_history([shared, earlier], pity=20))
        self.assertEqual(counts["角色跃迁"], 160)
        self.assertEqual([x["time"] for x in pools["角色跃迁"]["list"]], [earlier["time"], first["time"]])

    def test_older_official_pity_does_not_overwrite_newer_legacy_tail(self):
        old = legacy_history()
        shared = next(x for x in old["data"]["角色跃迁"] if x["rank_type"] == "5")
        new = official_history([official_record(80, "姬子", shared["id"], shared["time"])], pity=3)
        new["pool_data_time"] = {"角色跃迁": "2026-01-01 01:25:00"}
        pools, counts = self.stats.build_gacha_statistics(old, new)
        self.assertEqual(pools["角色跃迁"]["remain"], 20)
        self.assertEqual(counts["角色跃迁"], 100)

    def test_official_only_empty_pool_keeps_pity_in_total(self):
        pools, counts = self.stats.build_gacha_statistics({}, official_history([], pity=35))
        self.assertEqual(counts["角色跃迁"], 35)
        self.assertEqual(pools["角色跃迁"]["total"], 0)
        self.assertEqual(pools["角色跃迁"]["avg"], 0)

    def test_official_only_partial_refresh_keeps_failed_pool_pity(self):
        new = official_history([], pity=63)
        new["pool_data_time"] = {"角色跃迁": "2026-01-01 13:00:00"}
        # Older renderer versions supplied this empty legacy placeholder.
        placeholder = {"data": {}, "data_time": new["data_time"], "char_gacha_num": 0}
        pools, counts = self.stats.build_gacha_statistics(placeholder, new)
        self.assertEqual(pools["角色跃迁"]["remain"], 63)
        self.assertEqual(counts["角色跃迁"], 63)

    def test_legacy_only_keeps_total_and_empty_pools(self):
        pools, counts = self.stats.build_gacha_statistics(legacy_history(), {})
        self.assertEqual(counts["角色跃迁"], 100)
        self.assertEqual(pools["角色跃迁"]["avg"], 80)
        self.assertEqual(counts["光锥跃迁"], 0)
        self.assertEqual(len(pools), 6)


if __name__ == "__main__":
    unittest.main()
