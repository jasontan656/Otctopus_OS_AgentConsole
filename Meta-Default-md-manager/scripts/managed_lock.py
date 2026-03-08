from __future__ import annotations

import fcntl
from contextlib import contextmanager
from pathlib import Path

from managed_paths import lock_path


@contextmanager
def acquire_cli_lock(skill_root: Path, command_name: str):
    path = lock_path(skill_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+", encoding="utf-8")
    try:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(
                f"Meta-Default-md-manager command lock busy: `{command_name}` cannot run while another stage is running"
            ) from exc
        handle.seek(0)
        handle.truncate(0)
        handle.write(f"{command_name}\n")
        handle.flush()
        yield
    finally:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()
