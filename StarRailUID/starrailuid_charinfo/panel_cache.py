from datetime import UTC, datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from gsuid_core.logger import logger
from msgspec import json as msgjson
from starrail_damage_cal.model import MihomoCharacter

from ..utils.resource.RESOURCE_PATH import PLAYER_PATH


def save_panel_metadata(uid: str, chars: dict[str, MihomoCharacter], source: str) -> None:
    """Keep source metadata in character JSON even with older damage-cal versions."""
    updated_at = datetime.now(UTC).isoformat(timespec="seconds")
    for char in chars.values():
        # New converters already persisted both fields atomically.
        if getattr(char, "source", "") == source and getattr(char, "updated_at", ""):
            continue
        data = msgjson.decode(msgjson.encode(char))
        data.update(source=source, updated_at=updated_at)
        path = PLAYER_PATH / str(uid) / f"{char.avatarName}.json"
        with NamedTemporaryFile(dir=path.parent, suffix=".tmp", delete=False) as file:
            temporary = Path(file.name)
            try:
                file.write(msgjson.encode(data))
                file.close()
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)


def panel_updated_at(char: MihomoCharacter, uid: str, source: str) -> str:
    if source not in ("mys", "mihomo"):
        return ""
    value = getattr(char, "updated_at", "")
    if not value:
        path = PLAYER_PATH / str(uid) / f"{char.avatarName}.json"
        try:
            data = msgjson.decode(path.read_bytes())
        except (OSError, ValueError) as exc:
            logger.warning(f"[sr面板] 缓存更新时间读取失败: {path}, error={exc}")
            return ""
        if data.get("source") != source:
            return ""
        value = data.get("updated_at", "")
    if not value:
        return ""
    try:
        updated = datetime.fromisoformat(value)
        if updated.tzinfo is None:
            return ""
        return updated.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    except (TypeError, ValueError):
        return ""


def panel_watermark(source: str) -> str:
    labels = {
        "mys": "Data from MiYouShe",
        "mihomo": "Thank for mihomo.me",
        "self": "Local simulated panel",
        "simulated": "Simulated panel",
    }
    label = labels.get(source, "Cached panel - source unknown")
    return f"--Created by qwerdvd-Designed By Wuyi-{label}--"
