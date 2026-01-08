from __future__ import annotations
from dataclasses import dataclass
from logging import Logger
from playwright.sync_api import Page

from ..models.user import User
from ..pages.inventory_page import InventoryPage
from ..pages.login_page import LoginPage
from .config import Config


@dataclass
class Application:
    """Simple DI container for pages and services bound to a Playwright Page."""

    page: Page
    config: Config
    logger: Logger

    @property
    def login_page(self) -> LoginPage:
        return LoginPage(self.page, self.config, self.logger)

    @property
    def inventory_page(self) -> InventoryPage:
        return InventoryPage(self.page, self.config, self.logger)

    def login_as(self, user: User) -> None:
        self.logger.info("[FLOW] Login as %s", user.username)
        self.login_page.open()
        self.login_page.login(user)
        self.inventory_page.wait_loaded()
