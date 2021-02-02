from typing import List, Tuple, Any
from buycoins.client import execute_query
from .orders import OrderType, _make_order


def place_limit_order(
    *,
    side: str,
    coin_amount: float,
    cryptocurrency: str,
    price_type: str,
    static_price: float = None,
    dynamic_exchange_rate: float = None,
):
    query_str = """
        mutation($side: OrderSide!, $amount: BigDecimal!, $crypto: Cryptocurrency, $type_: PriceType!, 
                 $static_price: BigDecimal!, $dynamic_exchange_rate: BigDecimal) {
          postLimitOrder(orderSide: $side, coinAmount: $amount, cryptocurrency: $crypto, %s, priceType: $type_){
            id
            cryptocurrency
            coinAmount
            side
            status 
            createdAt
            pricePerCoin
            priceType
            staticPrice
            dynamicExchangeRate
          }
        }    
    """ % (
        (
            "staticPrice: $static_price"
            if price_type == "static"
            else "dynamicExchangeRate: $dynamic_exchange_rate"
        )
    )

    variables = dict(
        side=side,
        amount=coin_amount,
        crypto=cryptocurrency,
        type_=price_type,
        static_price=static_price,
        dynamic_exchange_rate=dynamic_exchange_rate,
    )
    result = execute_query(query_str, variables)
    return _make_order(result["postLimitOrder"])


def place_market_order(*, side: str, coin_amount: float, cryptocurrency: str):
    query_str = """
        mutation($side: OrderSide!, $amount: BigDecimal!, $crypto: Cryptocurrency) {
          postMarketOrder(orderSide: $side, coinAmount: $amount, cryptocurrency: $crypto){
            id
            cryptocurrency
            coinAmount
            side
            status 
            createdAt
            pricePerCoin
            priceType
            staticPrice
            dynamicExchangeRate
          }
        }
    """
    variables = dict(side=side, amount=coin_amount, crypto=cryptocurrency)
    result = execute_query(query_str, variables)
    return _make_order(result["postMarketOrder"])


def get_orders(status: str) -> Tuple[List[OrderType], Any]:
    query_str = """
        query($status: GetOrdersStatus!) {
          getOrders(status: $status) {
          dynamicPriceExpiry
            orders {
              edges {
                node {
                  id
                  cryptocurrency
                  coinAmount
                  side
                  status
                  createdAt
                  pricePerCoin
                  priceType
                  staticPrice
                  dynamicExchangeRate
                }
              }
            }
          }
        }
    """
    variables = dict(status=status)
    result = execute_query(query_str, variables)
    _res = result["getOrders"]

    orders = []
    for o in _res["orders"]["edges"]:
        orders.append(_make_order(o["node"]))
    return orders, _res["dynamicPriceExpiry"]


def get_market_book():
    query_str = """
        query {
          getMarketBook {
            dynamicPriceExpiry
            orders {
              edges {
                node {
                  id
                  cryptocurrency
                  coinAmount
                  side
                  status 
                  createdAt
                  pricePerCoin
                  priceType
                  staticPrice
                  dynamicExchangeRate
                }
              }
            }
          }
        }    
    """
    result = execute_query(query_str)
    _res = result["getMarketBook"]

    orders = []
    for o in _res["orders"]["edges"]:
        orders.append(_make_order(o["node"]))
    return orders, _res["dynamicPriceExpiry"]
