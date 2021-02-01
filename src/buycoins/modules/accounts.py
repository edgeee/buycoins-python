from typing import NamedTuple

from buycoins.client import execute_query


class VirtualDepositAccountType(NamedTuple):
    account_number: str
    account_name: str
    account_type: str
    bank_name: str
    account_reference: str


def create_deposit(account_name: str) -> VirtualDepositAccountType:
    query_str = """
        mutation($name: String!) {
          createDepositAccount(accountName: $name) {
            accountNumber
            accountName
            accountType
            bankName
            accountReference
         }
       }
    """

    result = execute_query(query_str, dict(name=account_name))
    account = result["createDepositAccount"]
    return VirtualDepositAccountType(
        account["accountNumber"],
        account["accountName"],
        account["accountType"],
        account["bankName"],
        account["accountReference"],
    )
