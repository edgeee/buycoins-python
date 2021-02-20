from buycoins.client import execute_query
from typing import NamedTuple, List, Optional
from decimal import Decimal


class CoinBalanceType(NamedTuple):
    id: str
    cryptocurrency: str
    confirmed_balance: Decimal


class NetworkFeeType(NamedTuple):
    estimated_fee: Decimal
    total: Decimal


class TransactionType(NamedTuple):
    hash: str
    id: str


class SendReturnValueType(NamedTuple):
    id: str
    address: str
    cryptocurrency: str
    amount: Decimal
    fee: Decimal
    status: str
    transaction: TransactionType


class AddressType(NamedTuple):
    cryptocurrency: str
    address: str


def get_balances() -> List[CoinBalanceType]:
    query_str = """
        query {
          getBalances{
            id
            cryptocurrency
            confirmedBalance
          }
        }
    """
    result = execute_query(query_str)
    balances = []
    for bal in result["getBalances"]:
        balances.append(
            CoinBalanceType(
                id=bal["id"],
                cryptocurrency=bal["cryptocurrency"],
                confirmed_balance=Decimal(bal["confirmedBalance"]),
            )
        )
    return balances


def get_balance(cryptocurrency: str) -> Optional[CoinBalanceType]:
    for balance in get_balances():
        if balance.cryptocurrency == cryptocurrency:
            return balance
    return None


def estimate_network_fee(cryptocurrency: str, amount: float) -> NetworkFeeType:
    query_str = """
        query($crypto: Cryptocurrency, $amount: BigDecimal!) {
          getEstimatedNetworkFee(cryptocurrency: $crypto, amount: $amount) {
            estimatedFee
            total
          }
        }
    """
    variables = dict(crypto=cryptocurrency, amount=amount)
    res = execute_query(query_str, variables)
    fee = res["getEstimatedNetworkFee"]

    return NetworkFeeType(
        estimated_fee=Decimal(fee["estimatedFee"]), total=Decimal(fee["total"])
    )


def send(*, cryptocurrency: str, amount: float, address: str) -> SendReturnValueType:
    query_str = """
        mutation($crypto: String!, $amount: Number!, $address: String!) {
          send(cryptocurrency: $crypto, amount: $amount, address: $address) {
            id
            address
            amount
            cryptocurrency
            fee
            status
            transaction {
              txhash
              id
            }
          }
        }    
    """
    variables = dict(crypto=cryptocurrency, amount=amount, address=address)
    res = execute_query(query_str, variables)
    send_val = res["send"]
    return SendReturnValueType(
        id=send_val["id"],
        address=send_val["address"],
        amount=Decimal(send_val["amount"]),
        cryptocurrency=send_val["cryptocurrency"],
        fee=Decimal(send_val["fee"]),
        status=send_val["status"],
        transaction=TransactionType(
            id=send_val["transaction"]["id"],
            hash=send_val["transaction"]["txhash"],
        ),
    )


def create_address(cryptocurrency: str):
    query_str = """
        mutation($crypto: Cryptocurrency) {
          createAddress(cryptocurrency: $crypto) {
            cryptocurrency
            address
          }
        }
    """
    variables = dict(crypto=cryptocurrency)
    res = execute_query(query_str, variables)
    res = res["createAddress"]
    return AddressType(cryptocurrency=res["cryptocurrency"], address=res["address"])
