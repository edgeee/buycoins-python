import json


def _make_graphql_response(resp: dict):
    return json.dumps(dict(data=resp))
