from tests.utils import _mock_gql


create_deposit_response = dict(
    createDepositAccount=dict(
        accountNumber="123",
        accountName="john doe",
        accountType="deposit",
        bankName="Providus",
        accountReference="ref",
    )
)


def test_create_deposit(_graphql_endpoint):
    from buycoins import accounts

    _mock_gql(create_deposit_response)

    acc = accounts.create_deposit("john doe")
    assert type(acc) == accounts.VirtualDepositAccountType
    assert acc.account_number == "123"
    assert acc.account_reference == "ref"
    assert acc.account_name == "john doe"
