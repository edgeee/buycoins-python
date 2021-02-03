from tests.utils import _mock_gql


place_limit_order_response = dict(
    postLimitOrder=dict(
        id="3",
        cryptocurrency="bitcoin",
        coinAmount="0.0023",
        side="buy",
        status="active",
        createdAt="2342343",
        pricePerCoin="29048",
        priceType="static",
        staticPrice="2342.23",
        dynamicExchangeRate=None,
    )
)

place_market_order_response = dict(
    postMarketOrder=dict(
        id="20",
        cryptocurrency="ethereum",
        coinAmount="0.0123",
        side="sell",
        status="active",
        createdAt="2342343",
        pricePerCoin="29048",
        priceType=None,
        staticPrice=None,
        dynamicExchangeRate=None,
    )
)


get_orders_response = dict(
    getOrders=dict(
        dynamicPriceExpiry="2340782074",
        orders=dict(
            edges=[
                dict(
                    node=dict(
                        id="4",
                        cryptocurrency="bitcoin",
                        coinAmount="0.2023",
                        status="active",
                    )
                ),
                dict(
                    node=dict(
                        id="2",
                        cryptocurrency="ethereum",
                        coinAmount="3.0",
                        status="active",
                    )
                ),
                dict(
                    node=dict(
                        id="2",
                        cryptocurrency="litecoin",
                        coinAmount="7.340",
                        status="active",
                    )
                ),
            ]
        ),
    )
)

get_market_book_response = dict(
    getMarketBook=dict(
        dynamicPriceExpiry="2340782074",
        orders=dict(
            edges=[
                dict(
                    node=dict(
                        id="2",
                        cryptocurrency="ethereum",
                        coinAmount="3.0",
                        status="active",
                    )
                ),
                dict(
                    node=dict(
                        id="2",
                        cryptocurrency="litecoin",
                        coinAmount="7.340",
                        status="active",
                    )
                ),
            ]
        ),
    )
)


def test_place_limit_order():
    from buycoins import p2p, orders

    _mock_gql(place_limit_order_response)

    order = p2p.place_limit_order(
        side="buy",
        coin_amount=0.0023,
        cryptocurrency="bitcoin",
        price_type="static",
        static_price=2342.23,
    )
    assert orders.OrderType == type(order)
    assert order.coin_amount == "0.0023"
    assert order.cryptocurrency == "bitcoin"
    assert order.price_type == "static"
    assert order.static_price == "2342.23"


def test_post_market_order():
    from buycoins import p2p, orders

    _mock_gql(place_market_order_response)

    order = p2p.place_market_order(
        side="sell", coin_amount=0.0123, cryptocurrency="ethereum"
    )
    assert isinstance(order, orders.OrderType)
    assert order.id == "20"
    assert order.side == "sell"
    assert order.cryptocurrency == "ethereum"
    assert order.price_type is None
    assert order.dynamic_exchange_rate is None
    assert order.static_price is None


def test_get_orders():
    from buycoins import p2p
    from buycoins.modules.orders import OrderType

    _mock_gql(get_orders_response)
    orders, price_expiry = p2p.get_orders(status="active")

    assert price_expiry == "2340782074"
    assert 3 == len(orders)
    assert orders[0].cryptocurrency == "bitcoin"
    assert isinstance(orders[0], OrderType)
    assert all(order.status == "active" for order in orders)


def test_get_market_book():
    from buycoins import p2p
    from buycoins.modules.orders import OrderType

    _mock_gql(get_market_book_response)

    orders, price_expiry = p2p.get_market_book()
    assert price_expiry == "2340782074"
    assert 2 == len(orders)
    assert isinstance(orders[0], OrderType)
