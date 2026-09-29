import asyncio
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

_refresh_locks: dict[str, asyncio.Lock] = {}


def refresh_lock(uid: str) -> asyncio.Lock:
    return _refresh_locks.setdefault(str(uid), asyncio.Lock())


def write_json_atomic(path: Path, data: dict) -> None:
    temporary_path = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = Path(file.name)
            json.dump(data, file, indent=2, ensure_ascii=False)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
