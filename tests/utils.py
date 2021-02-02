import json
from typing import Dict

import httpretty
from buycoins.client import BUYCOINS_GRAPHQL_ENDPOINT


def _make_graphql_response(resp: dict):
    return json.dumps(dict(data=resp))


def _mock_gql(response: Dict):
    httpretty.register_uri(
        httpretty.POST,
        BUYCOINS_GRAPHQL_ENDPOINT,
        status=200,
        body=_make_graphql_response(response),
    )
