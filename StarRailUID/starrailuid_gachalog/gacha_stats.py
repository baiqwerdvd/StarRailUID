"""Combine local full history and official five-star history for display."""

from datetime import datetime

CHANGE_MAP = {
    "始发跃迁": "begin",
    "群星跃迁": "normal",
    "角色跃迁": "char",
    "光锥跃迁": "weapon",
    "角色联动跃迁": "char_collabo",
    "光锥联动跃迁": "weapon_collabo",
}
NORMAL_LIST = [
    "彦卿",
    "白露",
    "姬子",
    "瓦尔特",
    "布洛妮娅",
    "克拉拉",
    "杰帕德",
    "银河铁道之夜",
    "以世界之名",
    "但战斗还未结束",
    "制胜的瞬间",
    "无可取代的东西",
    "时节不居",
    "如泥酣眠",
]

UP_LIST = {
    "希儿": [(2021, 2, 17, 18, 0, 0), (2025, 4, 9, 5, 59, 59)],
    "刃": [(2021, 2, 17, 18, 0, 0), (2025, 4, 9, 5, 59, 59)],
    "符玄": [(2021, 2, 17, 18, 0, 0), (2025, 4, 9, 5, 59, 59)],
    "云璃": [(2021, 2, 17, 18, 0, 0), (2026, 4, 22, 5, 59, 59)],
    "银枝": [(2021, 2, 17, 18, 0, 0), (2026, 4, 22, 5, 59, 59)],
    "银狼": [(2021, 2, 17, 18, 0, 0), (2026, 4, 22, 5, 59, 59)],
}


def check_up(name: str, _time: str) -> bool:
    for char in UP_LIST:
        if char == name:
            time = UP_LIST[char]
            e_time = datetime(*time[1])
            gacha_time = datetime.strptime(_time, "%Y-%m-%d %H:%M:%S")
            if gacha_time > e_time:
                return False
            return True
    return True


def _is_same_five_star_record(
    o: dict[str, str | int | bool],
    n: dict[str, str | int | bool],
) -> bool:
    o_id = str(o["id"]) if "id" in o else ""
    n_id = str(n["id"]) if "id" in n else ""
    if o_id and n_id and o_id == n_id:
        return True
    o_name = str(o["name"]) if "name" in o else ""
    n_name = str(n["name"]) if "name" in n else ""
    if o_name and n_name and o_name == n_name and len(o_id) >= 10 and len(n_id) >= 10:
        return o_id[:10] == n_id[:10]
    return False


def _infer_up(record: dict) -> bool:
    if record.get("is_up") is not None:
        return bool(record["is_up"])
    name = record["name"]
    if name in NORMAL_LIST:
        return False
    if name in UP_LIST:
        return check_up(name, record["time"])
    return True


def _update_time(data: dict, pool: str) -> datetime | None:
    value = data.get("pool_data_time", {}).get(pool, data.get("data_time", ""))
    for pattern in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H-%M-%S"):
        try:
            return datetime.strptime(value, pattern)
        except ValueError:
            continue
    return None


def _record_order(record: dict) -> tuple[str, int]:
    record_id = str(record.get("id", ""))
    return str(record.get("time", "")), int(record_id) if record_id.isdigit() else 0


def build_gacha_statistics(legacy: dict, official: dict) -> tuple[dict, dict[str, int]]:
    """Merge each five-star once, then sum its interval plus the current pity."""
    pools = {}
    counts = {}
    for pool, code in CHANGE_MAP.items():
        records = legacy.get("data", {}).get(pool, [])
        old_fives = []
        old_pity = 0
        for item in reversed(records):
            old_pity += 1
            if str(item["rank_type"]) == "5":
                old_fives.append(dict(item, gacha_num=old_pity, is_up=_infer_up(item)))
                old_pity = 0

        official_fives = []
        for item in reversed(official.get("data", {}).get(pool, [])):
            official_fives.append(
                dict(item, gacha_num=int(item.get("gacha_count", 0)), is_up=_infer_up(item))
            )

        merged = [dict(item) for item in old_fives]
        matched = set()
        for item in official_fives:
            for index, old in enumerate(old_fives):
                if index not in matched and _is_same_five_star_record(old, item):
                    # Official intervals and UP flags also correct matching old records.
                    merged[index].update(item)
                    matched.add(index)
                    break
            else:
                merged.append(item)
        merged.sort(key=_record_order)

        use_official_pity = pool in official.get("pity_counts", {})
        old_time = _update_time(legacy, pool)
        new_time = _update_time(official, pool)
        if records and old_time and new_time:
            use_official_pity = use_official_pity and new_time >= old_time
        elif old_fives and official_fives:
            use_official_pity = use_official_pity and _record_order(official_fives[-1]) >= _record_order(
                old_fives[-1]
            )
        remain = int(official["pity_counts"][pool]) if use_official_pity else old_pity

        old_total = int(legacy.get(f"{code}_gacha_num", len(records)))
        # Retain any total known beyond the stored full-history list, without
        # counting the legacy unfinished interval again after a new five-star.
        offset = max(old_total - len(records), 0) if records or not official_fives else 0
        intervals = [int(item["gacha_num"]) for item in merged]
        counts[pool] = offset + sum(intervals) + remain
        known = [item for item in merged if item["gacha_num"] > 0]
        known_pulls = sum(item["gacha_num"] for item in known)
        up_count = sum(item["is_up"] for item in known)
        times = [str(item["time"]) for item in [*records, *official_fives] if item.get("time")]
        start, end = (min(times), max(times)) if times else ("", "")
        pools[pool] = {
            "total": len(merged),
            "avg": round(known_pulls / len(known), 2) if known else 0,
            "avg_up": round(known_pulls / up_count, 2) if up_count else 0,
            "remain": remain,
            "list": merged,
            "time_range": f"{start}~{end}" if start != end else start,
        }
    return pools, counts
