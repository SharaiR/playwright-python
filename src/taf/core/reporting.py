from __future__ import annotations
from pathlib import Path
from typing import Optional

try:
    import allure  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - optional dependency
    allure = None


def attach_file(path: Path, name: Optional[str] = None, mime: Optional[str] = None) -> None:
    if not path.exists():
        return
    if allure is None:
        return
    allure.attach(
        path.read_bytes(),
        name=name or path.name,
        attachment_type=(
            allure.attachment_type.MP4 if (mime == "video/mp4" or path.suffix == ".mp4") else allure.attachment_type.PNG
        ),
    )
