from base64 import b64encode
from typing import Optional, Dict

from gql import Client, gql
from gql.transport import Transport
from gql.transport.requests import RequestsHTTPTransport

from buycoins.exceptions import NoConnectionError, ExecutionError, RemoteServerError


BUYCOINS_GRAPHQL_ENDPOINT = "https://backend.buycoins.tech/api/graphql"


_transport: Optional[Transport] = None
_client: Optional[Client] = None


def _make_auth_header(public_key, secret_key):
    return "Basic " + b64encode(bytes(f"{public_key}:{secret_key}", "utf8")).decode()


def initialize(public_key: str, secret_key: str):
    global _transport, _client
    if not _client:
        headers = {"Authorization": _make_auth_header(public_key, secret_key)}
        _transport = RequestsHTTPTransport(
            url=BUYCOINS_GRAPHQL_ENDPOINT, headers=headers
        )
        _client = Client(transport=_transport, fetch_schema_from_transport=False)


def get_client() -> Client:
    if not _client:
        raise NoConnectionError
    return _client


def execute_query(document: str, variables: Optional[Dict] = None) -> Dict:
    kwargs = {}
    if variables is not None:
        kwargs["variable_values"] = variables
    try:
        return get_client().execute(gql(document), **kwargs)
    except Exception as exc:
        if hasattr(exc, "errors") and len(exc.errors) > 0: # noqa
            raise ExecutionError(exc.errors[0]["message"])
        else:
            raise RemoteServerError(exc)
