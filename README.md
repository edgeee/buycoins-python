# Buycoins Python Library

[![Build Status](https://travis-ci.com/edgeee/buycoins-python.svg?token=oQSNV8eQ1aycrRUjPbyg&branch=main)](https://travis-ci.com/edgeee/buycoins-python) [![Circle CI](https://img.shields.io/badge/license-MIT-blue.svg)](https://img.shields.io/badge/license-MIT-blue.svg) [![PyPI version](https://badge.fury.io/py/buycoins.svg)](https://badge.fury.io/py/buycoins) [![Python 3.6+](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

This library provides easy access to the Buycoins API using the Python programming language. It provides all the feature of the API so that you don't need to interact with the API directly. This library can be used with Python 3.6+

## Table of Contents
* [Links](#links)
* [Installation](#installation)
* [Introduction](#introduction)
  * [Primer](#primer)
  * [Initialization](#initialization)   
* [Accounts](#accounts)
  * [Create Naira deposit account](#create-naira-deposit-account)
* [Orders](#orders)
  * [Get cryptocurrency prices](#get-cryptocurrency-prices)
  * [Get price for single cryptocurrency](#get-single-cryptocurrency-price)
  * [Buy a cryptocurrency](#buy-a-cryptocurrency)
  * [Sell a cryptocurrency](#sell-a-cryptocurrency)
* [P2P Trading](#p2p-trading)
  * [Place limit orders](#place-limit-orders)
  * [Place market order](#place-market-orders)
  * [Get list of orders](#get-list-of-orders)
  * [Get market book](#get-market-book)
* [Transactions](#transactions)
  * [Get cryptocurrency balances](#get-balances)
  * [Get single balance](#get-single-balance)
  * [Estimate network fee](#estimate-network-fee)  
  * [Create wallet address](#create-wallet-address)
  * [Send cryptocurrency](#send-cryptocurrency-to-an-address)
* [Webhooks](#webhooks)
  * [Verify event payload](#verify-event-payload)
* [Contributing](#contributing)
* [License](#license)
    
    

## Links
- Buycoins API documentation: https://developers.buycoins.africa/

## Installation
You can install this package using pip:
```sh
pip install --upgrade buycoins
```

## Introduction

#### Primer
- The library is structured around the concept of a `type`, so everything is a type. 
- All date quantities are specified as timestamps. So you would have to reconstruct the ISO dates yourself if you ever need to. 
- All cryptocurrency (and monetary) values are specified as decimals.
- Supports all cryptocurrencies supported by Buycoins

#### Initialization
Firstly, request API access by sending an email to  [support@buycoins.africa](mailto:support@buycoins.africa) with the email address you used in creating a Buycoins account.
When you've been granted access, you should be able to generate a public and secret key from the 'API settings' section of your account.

You have to initialize the library once in your app. You can do this when initializing databases, logging, etc.
As a security practice, it is best not to hardcode your API keys. You should store them in environmental variables or a remote Secrets Manager.

```python
import buycoins

buycoins.initialize('<PUBLIC-KEY>', '<SECRET-KEY>')
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

#### Create Naira deposit account
```python
import buycoins as bc

acc = bc.accounts.create_deposit('john doe')  # VirtualDepositAccountType

print(acc.account_name)  # john doe
print(acc.bank_name)  # bank name
print(acc.account_number)  # account number
print(acc.account_reference) # account reference
print(acc.account_type) # account type
```

### Orders
Orders provide a way to buy from and sell directly to Buycoins.
When buying or selling, price ID should be the ID gotten from calling either `.get_price()` or `.get_prices()`.
Make sure to use price that hasn't expired yet, so call `.get_price(cryptocurrency)` to get the latest price for the cryptocurrency just before buying or selling.


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

#### Get cryptocurrency prices
```python
import buycoins as bc

# Get prices of all cryptocurrencies
prices = bc.orders.get_prices()  # CoinPriceType[]

print(prices[0].id)  # ID of first price entry
print(prices[0].cryptocurrency)  # cryptocurrency
print(prices[0].expires_at)  # when this price entry will expire
print(prices[0].buy_price_per_coin)  # coin price
print(prices[0].min_buy)  # minimum amount you can buy
print(prices[0].max_buy)  # max amount you can buy
```

#### Get single cryptocurrency price
```python
import buycoins as bc

price = bc.orders.get_price('bitcoin')  # CoinPriceType

print(price.id)  # ID of price entry
print(price.cryptocurrency)  # cryptocurrency
print(price.expires_at)  # when this price entry will expire
print(price.buy_price_per_coin)  # coin price
print(price.min_buy)  # minimum amount you can buy
print(price.max_buy)  # max amount you can buy
```

#### Buy a cryptocurrency
```python
import buycoins as bc


order = bc.orders.buy(
    price_id='price-id',
    coin_amount=1.52,
    cryptocurrency='litecoin'
)  # OrderType

print(order.id)  # Order ID
print(order.status)  # either active or inactive
print(order.side)  # buy
print(order.cryptocurrency)  # litecoin
print(order.total_coin_amount)  # Total coin amount
print(order.price_type)  # Price type
```

#### Sell a cryptocurrency
```python
import buycoins as bc


order = bc.orders.sell(
    price_id='price-id',
    coin_amount=0.0043,
    cryptocurrency='ethereum'
)  # OrderType

print(order.id)  # Order ID
print(order.status)  # either active or inactive
print(order.side)  # sell
print(order.cryptocurrency)  # litecoin
print(order.total_coin_amount)  # Total coin amount
print(order.price_type)  # Price type
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

### Place limit orders
When placing limit orders, if `price_type` is `static`, `static_price` must also be specified, and if `price_type` is `dynamic`, `dynamic_exchange_rate` must be provided.

```python
import buycoins as bc


order = bc.p2p.place_limit_order(
    side='buy', # either 'buy' or 'sell'
    coin_amount=0.00043,
    cryptocurrency='ethereum',
    price_type='static',
    static_price=0.004,
    dynamic_exchange_rate=None  # float   
)  # OrderType

print(order.id)  # Order ID
print(order.status)  # status, either active or inactive
print(order.cryptocurrency)  # bitcoin, litecoin, etc
print(order.coin_amount)  # coin amount
```

#### Place market orders
```python
import buycoins as bc


# Place market order
# `order` has all the properties as shown above
order = bc.p2p.place_market_order(
    side='buy',  # either buy or sell
    coin_amount=0.00023,
    cryptocurrency='litecoin'
)  # order is an OrderType

print(order.id)  # Order ID
print(order.status)  # status, either active or inactive
print(order.cryptocurrency)  # bitcoin, litecoin, etc
print(order.coin_amount)  # coin amount
```

#### Get list of orders
```python
import buycoins as bc


orders, dynamic_price_expiry = bc.p2p.get_orders('active')  # (OrderType[], timestamp)

print(dynamic_price_expiry)  # timestamp of when dynamic price expires
print(orders[0].id)  # ID of first order
print(orders[1].status)  # status of the first order
```


#### Get Market book
```python
import buycoins as bc


market_book, dynamic_price_expiry = bc.p2p.get_market_book()  # (OrderType[], timestamp)

print(dynamic_price_expiry)  # timestamp of when dynamic price expires
print(market_book[0].id)  # ID of first order
print(market_book[1].status)  # status of the first order
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

#### Get balances
```python
import buycoins as bc

balances = bc.transactions.get_balances()  # CoinBalanceType[]

print(balances[0].cryptocurrency)  # bitcoin, litecoin, etc
print(balances[0].confirmed_balance)  # the confirmed balance
```


#### Get single balance
```python
import buycoins as bc


balance = bc.transactions.get_balance('bitcoin')  # CoinBalanceType

print(balance.cryptocurrency)  # bitcoin
print(balance.confirmed_balance)  # the confirmed balance
```

#### Estimate network fee
```python
import buycoins as bc


fee = bc.transactions.estimate_network_fee(
    'bitcoin',  # cryptocurrency
    0.32,  # txn amount
)  # NetworkFeeType

print(fee.estimated_fee)  # estimated fee for txn
print(fee.total)   # total
```

#### Send cryptocurrency to an address
```python
import buycoins as bc


sent = bc.transactions.send(
    cryptocurrency='ethereum',
    amount=0.0023,
    address='<wallet-address>'
)  # SendReturnValueType

print(sent.fee)  # fee charged for the 'send' txn
print(sent.status) # status of the txn
print(sent.transaction.id)  # ID of the txn
print(sent.transaction.hash)  # txn hash
```

#### Create wallet address
```python
import buycoins as bc


addr = bc.transactions.create_address('bitcoin')  # AddressType

print(addr.address)  # Address string
print(addr.cryptocurrency)  # cryptocurrency
```


### Webhooks

Webhooks provides a way for Buycoins to inform you of events that take place on your account.
See the [Buycoins documentation](https://developers.buycoins.africa/webhooks/introduction) for  an introduction and the available events.

#### Verify event payload
Ensure that the webhook event originated from Buycoins

```python
import buycoins as bc


is_valid = bc.webhook.verify_payload(
    body='<raw request body from buycoins (in bytes)>',
    webhook_token='<webhook-token generated on buycoins>',
    header_signature='X-Webhook-Signature header'
)

print(is_valid)  # True if the event is from Buycoins, False otherwise.
```

## Testing
To run tests:

```shell
poetry run pytest
```


## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)


## License
[MIT License](https://github.com/edgeee/buycoins-python/blob/master/LICENSE)
