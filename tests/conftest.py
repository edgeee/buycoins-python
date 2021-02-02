import pytest
import httpretty

import buycoins
from buycoins.client import BUYCOINS_GRAPHQL_ENDPOINT


@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    httpretty.enable()
    buycoins.initialize("fake-public-key", "fake-secret-key")


@pytest.fixture(scope="module")
def _graphql_endpoint():
    return BUYCOINS_GRAPHQL_ENDPOINT
