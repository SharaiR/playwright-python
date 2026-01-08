from __future__ import annotations
from logging import Logger
from playwright.sync_api import expect

from ..core.config import Config
from ..models.user import User
from .base_page import BasePage


class LoginPage(BasePage):
    _username = "#user-name"
    _password = "#password"
    _login_btn = "#login-button"
    _error = "[data-test='error']"

    def __init__(self, page, config: Config, logger: Logger) -> None:
        super().__init__(page, config, logger)

    def open(self) -> None:
        self.goto("/")
        expect(self.find(self._login_btn)).to_be_visible()

    def login(self, user: User) -> None:
        self.fill(self._username, user.username)
        self.fill(self._password, user.password)
        self.click(self._login_btn)

    def error_text(self) -> str:
        return self.find(self._error).inner_text()
