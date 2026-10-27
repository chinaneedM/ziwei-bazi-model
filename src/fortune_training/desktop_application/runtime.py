from __future__ import annotations

import sys
from pathlib import Path

from .distribution import REQUIRED_RUNTIME_REPOSITORY_FILES


class DesktopRuntimeError(RuntimeError):
    pass


def source_repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _validate_repository_root(root: Path) -> Path:
    resolved = root.resolve()
    missing = [
        relative
        for relative in REQUIRED_RUNTIME_REPOSITORY_FILES
        if not (resolved / relative).is_file()
    ]
    if missing:
        raise DesktopRuntimeError(
            "desktop runtime repository data missing: " + ", ".join(missing)
        )
    return resolved


def resolve_runtime_repository_root(
    *,
    resource_root: Path | None = None,
    packaged: bool | None = None,
) -> Path:
    """Resolve chart runtime data without consulting the process CWD.

    Source/development execution uses the checkout containing this module.
    PyInstaller execution uses ``sys._MEIPASS/runtime`` where the explicit
    repository-data inventory is bundled.
    """

    is_packaged = bool(getattr(sys, "frozen", False)) if packaged is None else packaged
    if is_packaged:
        if resource_root is None:
            raw = getattr(sys, "_MEIPASS", None)
            if raw is None:
                raise DesktopRuntimeError("packaged runtime is missing sys._MEIPASS")
            resource_root = Path(raw)
        return _validate_repository_root(Path(resource_root) / "runtime")

    root = source_repository_root() if resource_root is None else Path(resource_root)
    return _validate_repository_root(root)
