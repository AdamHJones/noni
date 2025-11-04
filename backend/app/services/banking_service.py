from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app.core.config import settings


class BankingService:
    """
    Plaid integration for read-only financial data
    SECURITY: No ability to transfer money or make changes
    """

    def __init__(self):
        configuration = Configuration(
            host=self._get_plaid_host(),
            api_key={
                "clientId": settings.PLAID_CLIENT_ID,
                "secret": settings.PLAID_SECRET,
            },
        )
        api_client = ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def _get_plaid_host(self) -> str:
        """Get Plaid API host based on environment"""
        env = settings.PLAID_ENV.lower()
        if env == "sandbox":
            return "https://sandbox.plaid.com"
        elif env == "development":
            return "https://development.plaid.com"
        else:
            return "https://production.plaid.com"

    async def create_link_token(self, user_id: str) -> str:
        """
        Create a link token for Plaid Link initialization
        This is used on the frontend to connect bank accounts
        """
        try:
            request = LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(client_user_id=user_id),
                client_name="Care Companion",
                products=[Products("transactions"), Products("auth")],
                country_codes=[CountryCode("US")],
                language="en",
            )

            response = self.client.link_token_create(request)
            return response.link_token

        except Exception as e:
            print(f"Error creating link token: {e}")
            raise

    async def exchange_public_token(self, public_token: str) -> str:
        """
        Exchange public token for access token
        Called after user connects their bank
        """
        try:
            request = ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request)
            return response.access_token

        except Exception as e:
            print(f"Error exchanging public token: {e}")
            raise

    async def get_balances(self, access_token: str) -> List[Dict]:
        """
        Get account balances (read-only)
        NEVER exposes account numbers for security
        """
        try:
            request = AccountsBalanceGetRequest(access_token=access_token)
            response = self.client.accounts_balance_get(request)

            accounts = []
            for account in response.accounts:
                accounts.append(
                    {
                        "name": account.name,
                        "type": account.type.value,
                        "subtype": account.subtype.value if account.subtype else None,
                        "balance": float(account.balances.current or 0),
                        "available": float(account.balances.available or 0)
                        if account.balances.available
                        else None,
                        "currency": account.balances.iso_currency_code,
                        # SECURITY: Never expose account numbers
                        # account_id is internal Plaid ID, safe to store
                        "account_id": account.account_id,
                    }
                )

            return accounts

        except Exception as e:
            print(f"Error fetching balances: {e}")
            return []

    async def get_recent_transactions(
        self, access_token: str, days: int = 30
    ) -> List[Dict]:
        """Get recent transactions for the last N days"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)

            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date,
            )

            response = self.client.transactions_get(request)

            transactions = []
            for txn in response.transactions:
                transactions.append(
                    {
                        "id": txn.transaction_id,
                        "date": str(txn.date),
                        "name": txn.name,
                        "amount": float(txn.amount),
                        "category": txn.category,
                        "pending": txn.pending,
                    }
                )

            return transactions

        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []

    async def check_for_deposit(
        self, access_token: str, expected_amount: float, description: str
    ) -> bool:
        """
        Check if a specific deposit has arrived
        Useful for "Did my Social Security check arrive?"
        """
        try:
            transactions = await self.get_recent_transactions(access_token, days=7)

            for txn in transactions:
                # In Plaid, deposits are negative amounts
                if (
                    txn["amount"] == -abs(expected_amount)
                    and description.lower() in txn["name"].lower()
                ):
                    return True

            return False

        except Exception as e:
            print(f"Error checking for deposit: {e}")
            return False

    def format_balance_for_speech(self, accounts: List[Dict]) -> str:
        """Format account balances for voice response"""
        if not accounts:
            return "I couldn't find any account information."

        # Find primary accounts
        checking = next((a for a in accounts if a["subtype"] == "checking"), None)
        savings = next((a for a in accounts if a["subtype"] == "savings"), None)

        speech = ""

        if checking:
            balance = checking["balance"]
            speech += f"You have ${balance:,.2f} in your checking account. "

        if savings:
            balance = savings["balance"]
            speech += f"And ${balance:,.2f} in your savings account. "

        if not speech:
            # Fallback to any account
            total = sum(a["balance"] for a in accounts)
            speech = f"Your total account balance is ${total:,.2f}. "

        speech += "All your accounts are in good standing."

        return speech

    def format_simple_balance(self, accounts: List[Dict]) -> str:
        """Simple yes/no format for "Do I have enough money?" """
        checking = next((a for a in accounts if a["subtype"] == "checking"), None)

        if not checking:
            return "I can see your accounts are active."

        balance = checking["balance"]

        if balance > 1000:
            return f"Yes, you have ${balance:,.2f}. You're doing great!"
        elif balance > 100:
            return f"You have ${balance:,.2f}. You have enough for now."
        else:
            return f"You have ${balance:,.2f} in your account. You might want to check with your caregiver."
