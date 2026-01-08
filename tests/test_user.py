from taf.models.user import User


def test_user_dataclass_roundtrip() -> None:
    user = User(username="standard_user", password="secret_sauce")

    assert user.username == "standard_user"
    assert user.password == "secret_sauce"
