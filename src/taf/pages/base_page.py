from __future__ import annotations
from logging import Logger
from typing import Final
from playwright.sync_api import Locator, Page
from ..core.config import Config


class BasePage:
    def __init__(self, page: Page, config: Config, logger: Logger) -> None:
        self.page: Final[Page] = page
        self.config = config
        self.logger = logger

    def goto(self, path: str = "/") -> None:
        url = self.config.base_url.rstrip("/") + path
        self.logger.info("Navigate to %s", url)
        self.page.goto(url)

    def find(self, selector: str) -> Locator:
        self.logger.info("Find element: %s", selector)
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        self.logger.info("Click: %s", selector)
        self.find(selector).click()

    def fill(self, selector: str, text: str) -> None:
        self.logger.info("Fill %s with '%s'", selector, text)
        self.find(selector).fill(text)

    def should_have_url(self, path: str) -> None:
        expected = self.config.base_url.rstrip("/") + path
        self.logger.info("Expect URL to be %s", expected)
        self.page.wait_for_url(expected)
