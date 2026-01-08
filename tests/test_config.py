from taf.core.config import Config


def test_config_creds_contains_expected_keys() -> None:
    creds = Config().creds

    assert creds["STANDARD_USER"]
    assert creds["LOCKED_OUT_USER"]
    assert creds["PROBLEM_USER"]
    assert creds["PERFORMANCE_USER"]
    assert creds["PASSWORD"]
