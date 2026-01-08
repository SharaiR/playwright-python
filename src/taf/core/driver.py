from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from .config import Config


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def runtime_options(pytestconfig: pytest.Config, config: Config):
    browser_opt = pytestconfig.getoption("--browser")
    if isinstance(browser_opt, (list, tuple)):
        browser_opt = browser_opt[0] if browser_opt else None
    headed = bool(pytestconfig.getoption("--headed"))
    headless_flag = bool(pytestconfig.getoption("--headless"))
    headless = config.headless
    if headed:
        headless = False
    if headless_flag:
        headless = True
    return {
        "browser": browser_opt or config.browser,
        "headless": headless,
    }


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, config: Config, runtime_options) -> Generator[Browser, None, None]:
    br_name = runtime_options["browser"]
    headless = runtime_options["headless"]
    browser_type = getattr(playwright_instance, br_name)
    if not Path(browser_type.executable_path).exists():
        subprocess.run([sys.executable, "-m", "playwright", "install", br_name], check=True)
    browser = browser_type.launch(headless=headless)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser, config: Config) -> Generator[BrowserContext, None, None]:
    config.ensure_artifacts()
    ctx = browser.new_context(record_video_dir=Path(config.video_dir))
    ctx.tracing.start(screenshots=True, snapshots=True, sources=False)
    yield ctx
    ctx.tracing.stop(path=Path(config.trace_dir) / "trace.zip")
    ctx.close()


@pytest.fixture()
def page(context: BrowserContext, config: Config) -> Generator[Page, None, None]:
    page = context.new_page()
    page.set_default_timeout(10_000)
    yield page
    page.close()
