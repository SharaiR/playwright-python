from __future__ import annotations
import pytest
from taf.core.di import Application
from taf.models.user import User


@pytest.mark.ui
@pytest.mark.regression
def test_add_to_cart_increments_badge(app: Application, config) -> None:
    user = User(username=config.creds["STANDARD_USER"], password=config.creds["PASSWORD"])
    app.login_as(user)
    app.inventory_page.add_to_cart("Sauce Labs Backpack")
    assert app.inventory_page.cart_count() == 1
