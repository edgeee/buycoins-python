from decimal import Decimal
from typing import NamedTuple, List, Dict, Optional

from buycoins.client import execute_query


class CoinPriceType(NamedTuple):
    id: str
    cryptocurrency: str
    buy_price_per_coin: Decimal
    min_buy: Decimal
    max_buy: Decimal
    expires_at: int


class OrderType(NamedTuple):
    id: str
    cryptocurrency: str
    status: str
    side: str
    created_at: int
    static_price: Decimal = None
    price_type: str = None
    dynamic_exchange_rate: str = None
    coin_amount: Decimal = None


def _make_order(node: Dict) -> OrderType:
    return OrderType(
        id=node.get("id"),
        cryptocurrency=node.get("cryptocurrency"),
        coin_amount=node.get("coinAmount", node.get("totalCoinAmount")),
        side=node.get("side"),
        status=node.get("status"),
        created_at=node.get("createdAt"),
        price_type=node.get("priceType"),
        static_price=node.get("staticPrice", 0),
        dynamic_exchange_rate=node.get("dynamicExchangeRate"),
    )


def get_prices() -> List[CoinPriceType]:
    query_str = """
        query {
          getPrices {
            id
            cryptocurrency
            buyPricePerCoin
            minBuy
            maxBuy
            expiresAt
          }
        }    
    """
    result = execute_query(query_str)
    prices = []
    for price in result["getPrices"]:
        record = CoinPriceType._make(
            [
                price["id"],
                price["cryptocurrency"],
                Decimal(price["buyPricePerCoin"]),
                Decimal(price["minBuy"]),
                Decimal(price["maxBuy"]),
                price["expiresAt"],
            ]
        )
        prices.append(record)
    return prices


def get_price(cryptocurrency) -> Optional[CoinPriceType]:
    for price in get_prices():
        if price.cryptocurrency == cryptocurrency:
            return price
    return None


def _do_order(order_type, *, price_id: str, coin_amount: float, cryptocurrency: str):
    query_str = (
        """
        mutation($price: ID!, $amount: BigDecimal!, $crypto: Cryptocurrency) {
          %s(price: $price, coin_amount: $amount, cryptocurrency: $crypto) {
            id
            cryptocurrency
            status
            totalCoinAmount
            side
            createdAt
          }
        }      
    """
        % order_type
    )

    variables = dict(price=price_id, amount=coin_amount, crypto=cryptocurrency)
    result = execute_query(query_str, variables)
    return _make_order(result[order_type])


def buy(*, price_id: str, coin_amount: float, cryptocurrency: str):
    return _do_order(
        "buy", price_id=price_id, coin_amount=coin_amount, cryptocurrency=cryptocurrency
    )


def sell(*, price_id: str, coin_amount: float, cryptocurrency: str) -> OrderType:
    return _do_order(
        "sell",
        price_id=price_id,
        coin_amount=coin_amount,
        cryptocurrency=cryptocurrency,
    )
