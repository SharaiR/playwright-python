from __future__ import annotations

import pytest
from taf.core.di import Application
from taf.models.user import User


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_login_success(app: Application, config) -> None:
    user = User(username=config.creds["STANDARD_USER"], password=config.creds["PASSWORD"])
    app.login_page.open()
    app.login_page.login(user)
    app.inventory_page.wait_loaded()


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out."),
        ("standard_user", "wrong", "Username and password do not match"),
    ],
)
def test_login_negative(app: Application, username: str, password: str, expected: str) -> None:
    app.login_page.open()
    app.login_page.login(User(username, password))
    assert expected.lower() in app.login_page.error_text().lower()
