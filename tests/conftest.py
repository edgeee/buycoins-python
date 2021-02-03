import pytest
import httpretty

import buycoins


@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    httpretty.enable()
    buycoins.initialize("fake-public-key", "fake-secret-key")
