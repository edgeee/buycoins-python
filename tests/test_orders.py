from decimal import Decimal
import httpretty

from tests.utils import _make_graphql_response


get_prices_response = dict(
    getPrices=[
        dict(
            id="1",
            cryptocurrency="bitcoin",
            buyPricePerCoin="5332823",
            minBuy=0.0001,
            maxBuy=0.04,
            expiresAt=2382084323,
        ),
        dict(
            id="2",
            cryptocurrency="litecoin",
            buyPricePerCoin="1993",
            minBuy=0.001,
            maxBuy=5.003,
            expiresAt=2382084323,
        ),
        dict(
            id="3",
            cryptocurrency="ethereum",
            buyPricePerCoin="24384",
            minBuy=0.02041,
            maxBuy=2,
            expiresAt=2382084323,
        ),
    ]
)

sell_coin_response = dict(
    sell=dict(
        id="1",
        cryptocurrency="ethereum",
        status="active",
        totalCoinAmount=0.0510,
        side="sell",
        createdAt=230238423,
    )
)

buy_response = dict(
    buy=dict(
        id="10",
        cryptocurrency="bitcoin",
        status="active",
        totalCoinAmount=0.3,
        side="buy",
        createdAt=230238423,
    )
)


def test_get_prices(_graphql_endpoint):
    from buycoins import orders

    httpretty.register_uri(
        httpretty.POST,
        _graphql_endpoint,
        status=200,
        body=_make_graphql_response(get_prices_response),
    )

    prices = orders.get_prices()
    assert 3 == len(prices)
    assert all(orders.CoinPriceType == type(price) for price in prices)
    assert prices[0].cryptocurrency == "bitcoin"
    assert prices[0].id == "1"


def test_get_price(_graphql_endpoint):
    from buycoins import orders

    httpretty.register_uri(
        httpretty.POST,
        _graphql_endpoint,
        status=200,
        body=_make_graphql_response(get_prices_response),
    )

    price = orders.get_price("litecoin")
    assert orders.CoinPriceType == type(price)
    assert price.cryptocurrency == "litecoin"
    assert price.id == "2"
    assert price.buy_price_per_coin == Decimal(1993)


def test_sell(_graphql_endpoint):
    from buycoins import orders

    httpretty.register_uri(
        httpretty.POST,
        _graphql_endpoint,
        status=200,
        body=_make_graphql_response(sell_coin_response),
    )

    resp = orders.sell(price_id="1", coin_amount=0.0510, cryptocurrency="ethereum")

    assert orders.OrderType == type(resp)
    assert resp.coin_amount == Decimal(0.0510)
    assert resp.status == "active"
    assert resp.cryptocurrency == "ethereum"


def test_buy(_graphql_endpoint):
    from buycoins import orders

    httpretty.register_uri(
        httpretty.POST,
        _graphql_endpoint,
        status=200,
        body=_make_graphql_response(buy_response),
    )

    buy_order = orders.buy(price_id="10", coin_amount=0.3, cryptocurrency="bitcoin")

    assert orders.OrderType == type(buy_order)
    assert buy_order.status == "active"
    assert buy_order.coin_amount == Decimal(0.3)
    assert buy_order.cryptocurrency == "bitcoin"
