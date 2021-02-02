from decimal import Decimal

from tests.utils import _mock_gql


get_balances_response = dict(
    getBalances=[
        dict(id="1", cryptocurrency="bitcoin", confirmedBalance="10.01"),
        dict(id="2", cryptocurrency="ethereum", confirmedBalance="2.304"),
        dict(id="3", cryptocurrency="litecoin", confirmedBalance="0.0233"),
    ]
)

estimate_network_fee_response = dict(
    getEstimatedNetworkFee=dict(estimatedFee="2322.3", total="2342.02")
)


send_crypto_response = dict(
    send=dict(
        id='1',
        address='addr',
        amount='0.3222',
        cryptocurrency='bitcoin',
        fee='0.0002',
        status='active',
        transaction=dict(
            id='tx1',
            hash='a49s038aty2sfa23434872'
        )
    )
)


create_address_response = dict(
createAddress=dict(
    cryptocurrency='litecoin',
    address='addr1'
)
)


def test_get_balances():
    from buycoins import transactions

    _mock_gql(get_balances_response)

    balances = transactions.get_balances()
    assert 3 == len(balances)
    assert all(isinstance(bal, transactions.CoinBalanceType) for bal in balances)
    assert balances[0].id == "1"
    assert balances[0].cryptocurrency == "bitcoin"
    assert balances[0].confirmed_balance == Decimal("10.01")


def test_get_balance():
    from buycoins import transactions

    _mock_gql(get_balances_response)

    balance = transactions.get_balance("litecoin")
    assert isinstance(balance, transactions.CoinBalanceType)
    assert balance.cryptocurrency == "litecoin"
    assert balance.id == "3"


def test_estimate_network_fees():
    from buycoins import transactions

    _mock_gql(estimate_network_fee_response)

    fee = transactions.estimate_network_fee("bitcoin", 0.0234)
    assert isinstance(fee, transactions.NetworkFeeType)
    assert fee.estimated_fee == Decimal("2322.3")
    assert fee.total == Decimal("2342.02")


def test_send_cryptocurrency():
    from buycoins import transactions

    _mock_gql(send_crypto_response)

    sent = transactions.send(cryptocurrency='bitcoin', amount=0.3222, address='addr')
    assert isinstance(sent, transactions.SendReturnValueType)
    assert sent.id == '1'
    assert sent.cryptocurrency == 'bitcoin'
    assert sent.amount == Decimal('0.3222')
    assert sent.transaction.id == 'tx1'


def test_create_address():
    from buycoins import transactions

    _mock_gql(create_address_response)

    created_address = transactions.create_address('litecoin')
    assert isinstance(created_address, transactions.AddressType)
    assert created_address.address == 'addr1'
    assert created_address.cryptocurrency == 'litecoin'
