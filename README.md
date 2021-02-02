# Buycoins Python Library

[![Build Status](https://travis-ci.com/edgeee/buycoins-python.svg?token=oQSNV8eQ1aycrRUjPbyg&branch=main)](https://travis-ci.com/edgeee/buycoins-python) [![Circle CI](https://img.shields.io/badge/license-MIT-blue.svg)](https://img.shields.io/badge/license-MIT-blue.svg) [![PyPI version](https://badge.fury.io/py/buycoins.svg)](https://badge.fury.io/py/buycoins) [![Python 3.6+](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

This library provides easy access to the Buycoins API using the Python programming language. It provides all the feature of the API so that you don't need to interact with the API directly. This libary can be used with Python 3.6+

## Links
1. Buycoins API documentation: https://developers.buycoins.africa/

## Installation
You can install this package using pip:
```sh
pip install --upgrade buycoins
```

## Documentation

### Primer
- The library is structured around the concept of a `type`, so everything is a type. 
- All date quantities are specified as timestamps. So you would have to reconstruct the ISO dates yourself if you ever need to. 
- All cryptocurrency (and monetary) values are specified as decimals.
- Currently supported cryptocurrencies are bitcoin, ethereum, & litecoin. To be updated as the Buycoins API evolves.

### Initialization
Firstly, request API access by sending an email to  [support@buycoins.africa](mailto:support@buycoins.africa) with the email address you used in creating a Buycoins account.
When you've been granted access, you should be able to generate a public and secret key from the "API settings" section of your account.

You have to initialize the library once in your app. You can do this when initializing databases, logging, etc.

```python
import buycoins

buycoins.initialize("<PUBLIC-KEY>", "<SECRET-KEY>")
```

### Accounts
Accounts provide a way to programmatically fund you Buycoins account.

#### Types
```dtd
VirtualDepositAccountType:
    account_number: str
    account_name: str
    account_type: str
    bank_name: str
    account_reference: str
```

#### Usage:
```python
import buycoins as bc

# Create a virtual deposit account:
acc = bc.accounts.create_deposit("john doe") # acc is a VirtualDepositAccountType

acc.account_name  # john doe
acc.bank_name  # bank name
acc.account_number  # account number
```

### Orders
Orders provide a way to buy from and sell directly to Buycoins.

#### Types
```dtd
CoinPriceType:
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
    total_coin_amount: str
    static_price: Decimal
    price_type: str
    dynamic_exchange_rate: str
    coin_amount: Decimal
```

#### Usage
```python
import buycoins as bc

# Get prices of all cryptocurrencies
prices = bc.orders.get_prices()  # prices is a list of CoinPriceType

prices[0].id  # ID of this price entry
prices[0].cryptocurrency  # cryptocurrency, e.g. bitcoin, litecoin
prices[0].expires_at  # when this price entry will expire


# Get price for a single cryptocurrency
price = bc.orders.get_price("bitcoin")  # price is a CoinPriceType

price.id  # ID of this price entry
price.cryptocurrency  # bitcoin


# Buy a cryptocurrency
order = bc.orders.buy(
    price_id="price-id",  # price ID from calling either .get_price() or .get_prices()
    coin_amount=1.52,
    cryptocurrency="litecoin"
)  # order is an OrderType

order.status   # either active or inactive
order.side   # either buy or sell
order.cryptocurrency   # litecoin


# Sell a cryptocurrency
order = bc.orders.sell(
    price_id="price-id",  # price ID from calling either .get_price() or .get_prices()
    coin_amount=0.0043,
    cryptocurrency="ethereum"
)  # order is an OrderType

order.status  # either active or pending
order.side  # sell
order.cryptocurrency  # ethereum
```

### P2P Trading
P2P Trading lets you trade cryptocurrencies with other users.
If you are not familiar with p2p trading on the Buycoins platform, read about it [here](https://developers.buycoins.africa/p2p/introduction)

#### Types
```dtd
class OrderType(NamedTuple):
    id: str
    cryptocurrency: str
    status: str
    side: str
    created_at: int
    total_coin_amount: str
    static_price: Decimal
    price_type: str
    dynamic_exchange_rate: str
    coin_amount: Decimal
```

#### Usage
```python
import buycoins as bc

# Place limit order
order = bc.p2p.place_limit_order(
    side="buy", # either "buy" or "sell"
    coin_amount=0.00043,
    cryptocurrency="ethereum",
    price_type="static",
    static_price=0.004,
    dynamic_exchange_rate=None  # float   
)  # order is an OrderType

# NB: if price_type == 'static', static_price must be provided, and 
# if price_type == 'dynamic', dynamic_exchange_rate must be provided

order.id  # ID of order
order.status  # status, either active or inactive


# Place market order
order = bc.p2p.place_market_order(
    side="buy",  # either buy or sell
    coin_amount=0.00023,
    cryptocurrency='litecoin'
)  # order is an OrderType

order.id  # ID of order
order.status  # status, either active or inactive


# Get a list of all your orders
orders, dynamic_price_expiry = bc.p2p.get_orders("active")  # orders is a list of OrderType; dynamic_price_expiry is a timestamp

orders[0].id  # ID of the first order
orders[1].status  # status of the first order


# Get a list of all ongoing orders on the Buycoins platform
market_book, dynamic_price_expiry = bc.p2p.get_market_book()  # market_book is a list of OrderType; dynamic_price_expiry is a timestamp

orders[0].id  # ID of the first order
orders[1].status  # status of the first order
```


### Transactions

Transactions enable you to send and receive cryptocurrencies.

#### Types
```dtd
CoinBalanceType:
    id: str
    cryptocurrency: str
    confirmed_balance: Decimal

NetworkFeeType:
    estimated_fee: Decimal
    total: Decimal

TransactionType:
    hash: str
    id: str

SendReturnValueType:
    id: str
    address: str
    cryptocurrency: str
    amount: Decimal
    fee: Decimal
    status: str
    transaction: TransactionType

AddressType:
    cryptocurrency: str
    address: str
```

#### Usage
```python
import buycoins as bc

# Get balances
balances = bc.transactions.get_balances()  # balances is a list of CoinBalanceType
balances[0].cryptocurrency  # bitcoin, litecoin, etc
balances[0].confirmed_balance  # the confirmed balance


# Get balance for a single cryptocurrency
balance = bc.transactions.get_balance("bitcoin")  # balance is a CoinBalanceType
balance.cryptocurrency  # bitcoin
balance.confirmed_balance  # the confirmed balance


# Estimate network fee required for a transaction
fee = bc.transactions.estimate_network_fee(
    "bitcoin",  # cryptocurrency
    0.0423,  # txn amount
)  # fee is a NetworkFeeType

fee.estimated_fee  # estimated fee for txn
fee.total  # total


# Send cryptocurrency to a wallet address
sent = bc.transactions.send(
    cryptocurrency="ethereum",
    amount=0.0023,
    address="<wallet-address>"
)  # sent is a SendReturnValueType

sent.fee  # fee charged for the "send" txn
sent.status # status of the txn
sent.transaction.id  # ID of the txn
sent.transaction.hash  # txn hash


# Generate wallet address
addr = bc.transactions.create_address("bitcoin")  # addr is an AddressType

addr.address  # Address string
addr.cryptocurrency  # cryptocurrency
```


## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)


## License
[MIT License](https://github.com/edgeee/buycoins-python/blob/master/LICENSE)
