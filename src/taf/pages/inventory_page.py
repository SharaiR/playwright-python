from __future__ import annotations
from logging import Logger
from playwright.sync_api import expect
from ..core.config import Config
from .base_page import BasePage


class InventoryPage(BasePage):
    _title = ".title:has-text('Products')"
    _cart_badge = ".shopping_cart_badge"

    def __init__(self, page, config: Config, logger: Logger) -> None:
        super().__init__(page, config, logger)

    def wait_loaded(self) -> None:
        expect(self.find(self._title)).to_be_visible()

    def add_to_cart(self, item_name: str) -> None:
        self.logger.info("Add to cart: %s", item_name)
        item = self.page.locator(".inventory_item").filter(has_text=item_name)
        item.locator("button:has-text('Add to cart')").click()

    def cart_count(self) -> int:
        badge = self.find(self._cart_badge)
        if badge.count() == 0:
            return 0
        text = badge.inner_text()
        return int(text)
