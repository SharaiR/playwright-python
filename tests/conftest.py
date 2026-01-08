from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse

import pytest
from playwright.sync_api import Page

from taf.core.config import Config
from taf.core.di import Application
from taf.core.logger import get_logger
from taf.core.reporting import attach_file

pytest_plugins = ["taf.core.driver"]


def _option_exists(parser: pytest.Parser, name: str) -> bool:
    groups = [getattr(parser, "_anonymous", None), *getattr(parser, "_groups", [])]
    for group in groups:
        if group is None:
            continue
        for option in getattr(group, "options", []):
            if name in option.names():
                return True
    return False


def _safe_addoption(parser: pytest.Parser, *args, **kwargs) -> None:
    if args and _option_exists(parser, args[0]):
        return
    try:
        parser.addoption(*args, **kwargs)
    except argparse.ArgumentError:
        # Avoid conflicts when another plugin registers the same option.
        pass


@pytest.hookimpl(trylast=True)
def pytest_addoption(parser: pytest.Parser) -> None:
    _safe_addoption(
        parser,
        "--browser",
        action="store",
        choices=["chromium", "firefox", "webkit"],
        help="Select browser (overrides BROWSER env)",
    )
    _safe_addoption(parser, "--headed", action="store_true", help="Run in headed mode (overrides HEADLESS)")
    _safe_addoption(parser, "--headless", action="store_true", help="Force headless mode")
    _safe_addoption(
        parser,
        "--test-type",
        action="store",
        choices=["all", "smoke", "regression"],
        default="all",
        help="Subset of tests to run",
    )
    _safe_addoption(parser, "--html", action="store", help="(optional) HTML report path")
    _safe_addoption(parser, "--self-contained-html", action="store_true", help="(optional) inline assets")
    _safe_addoption(parser, "--alluredir", action="store", help="(optional) Allure results dir")


def pytest_configure(config: pytest.Config) -> None:
    t = config.getoption("--test-type")
    if t == "smoke":
        config.option.markexpr = "smoke"
    elif t == "regression":
        config.option.markexpr = "regression"


@pytest.fixture(scope="session")
def config() -> Config:  # type: ignore[override]
    cfg = Config()
    cfg.ensure_artifacts()
    return cfg


@pytest.fixture()
def logger():
    return get_logger("taf.tests")


@pytest.fixture()
def app(page: Page, config: Config, logger) -> Application:
    return Application(page=page, config=config, logger=logger)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")  # type: ignore[assignment]
        config: Config = item.funcargs.get("config")  # type: ignore[assignment]
        if page is None:
            return
        ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        shot_path = Path(config.screenshot_dir) / f"{item.name}-{ts}.png"
        page.screenshot(path=str(shot_path), full_page=True)
        attach_file(shot_path, name=f"Screenshot: {item.name}")
        item.user_properties.append(("_needs_video", True))


@pytest.fixture(autouse=True)
def _attach_video_on_teardown(request: pytest.FixtureRequest, config: Config):
    yield
    try:
        if "page" not in request.fixturenames:
            return
        page: Page = request.getfixturevalue("page")
        need_video = dict(request.node.user_properties).get("_needs_video")
        if need_video and page.video is not None:
            video_path = page.video.path()  # type: ignore[assignment]
            if video_path:
                attach_file(Path(video_path), name=f"Video: {request.node.name}", mime="video/mp4")
    except Exception:
        pass
