# ruff: noqa: RUF001
"""Local resource inspection and persistent sync summaries; no network access."""

from collections.abc import Callable
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

from PIL import Image
from gsuid_core.logger import logger


def inspect_data(
    version_file: Path,
    resolve_file: Callable[[str], Path],
    calc_sha256: Callable[[Path], str],
    skipped: set[str],
) -> tuple[dict[str, Any] | None, list[str], int]:
    try:
        manifest = json.loads(version_file.read_text(encoding="utf-8"))
        if (
            not isinstance(manifest, dict)
            or not isinstance(manifest.get("version"), str)
            or not manifest["version"]
            or not isinstance(manifest.get("files"), dict)
            or not isinstance(manifest.get("file_names"), list)
            or not manifest["file_names"]
            or any(not isinstance(name, str) or Path(name).name != name for name in manifest["file_names"])
        ):
            return None, [version_file.name], 0
    except (OSError, ValueError):
        return None, [version_file.name], 0

    invalid = []
    names = set(manifest["file_names"]) - skipped
    if not names:
        return None, [version_file.name], 0
    for name in sorted(names):
        info = manifest["files"].get(name)
        sha = info.get("sha256") if isinstance(info, dict) else None
        try:
            if not sha or calc_sha256(resolve_file(name)) != sha:
                invalid.append(name)
        except OSError:
            invalid.append(name)
    return manifest, invalid, len(names)


def inspect_icons(label: str, mapping: Path, image_dir: Path) -> str:
    try:
        entries = json.loads(mapping.read_text(encoding="utf-8"))
        if not isinstance(entries, dict) or not entries or any(not key.isdecimal() for key in entries):
            return f"{label}: 未检查（核心映射缺失或损坏）"
    except (OSError, ValueError):
        return f"{label}: 未检查（核心映射缺失或损坏）"

    missing = invalid = 0
    for item_id in entries:
        path = image_dir / f"{item_id}.png"
        if not path.exists():
            missing += 1
            continue
        try:
            with Image.open(path) as image:
                image.verify()
        except (OSError, ValueError, SyntaxError):
            invalid += 1
    return f"{label}: 共 {len(entries)}，缺失 {missing}，损坏 {invalid}"


def save_sync_result(path: Path, status: str, stages: dict[str, str]) -> None:
    result = {
        "status": status,
        "time": datetime.now(UTC).isoformat(timespec="seconds"),
        "stages": stages,
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        temporary.replace(path)
    except OSError:
        logger.exception("保存星铁资源同步状态失败")


def last_sync_summary(path: Path) -> str:
    if not path.exists():
        return "最近同步: 尚未检查（无同步记录）"
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        timestamp = datetime.fromisoformat(record["time"]).isoformat(timespec="seconds")
        status = {"success": "成功", "failed": "失败", "running": "中断"}[record["status"]]
        stages = record["stages"]
        details = "、".join(
            name
            for name in ("图片资源", "数据文件", "光锥评价", "数据刷新")
            if stages.get(name) == "failed"
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return "最近同步: 未知（同步记录损坏）"
    suffix = f"；失败阶段: {details}" if details else ""
    return f"最近同步: {status}，{timestamp}{suffix}"
