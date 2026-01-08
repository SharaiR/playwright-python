from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

BrowserName = Literal["chromium", "firefox", "webkit"]


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


@dataclass(frozen=True)
class Config:
    base_url: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    headless: bool = _to_bool(os.getenv("HEADLESS"), True)
    browser: BrowserName = os.getenv("BROWSER", "chromium")  # type: ignore[assignment]

    artifacts_dir: Path = Path(os.getenv("ARTIFACTS_DIR", "artifacts"))
    video_dir: Path = Path(os.getenv("VIDEO_DIR", str(artifacts_dir / "videos")))
    screenshot_dir: Path = Path(os.getenv("SCREENSHOT_DIR", str(artifacts_dir / "screens")))
    trace_dir: Path = Path(os.getenv("TRACE_DIR", str(artifacts_dir / "traces")))

    @property
    def creds(self) -> dict[str, str]:
        return {
            "STANDARD_USER": os.getenv("STANDARD_USER", "standard_user"),
            "LOCKED_OUT_USER": os.getenv("LOCKED_OUT_USER", "locked_out_user"),
            "PROBLEM_USER": os.getenv("PROBLEM_USER", "problem_user"),
            "PERFORMANCE_USER": os.getenv("PERFORMANCE_USER", "performance_glitch_user"),
            "PASSWORD": os.getenv("PASSWORD", "secret_sauce"),
        }

    def ensure_artifacts(self) -> None:
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.video_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.trace_dir.mkdir(parents=True, exist_ok=True)
