from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.azure import AzureOpenAIChatClient
from pydantic import BaseModel, Field

import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data models (stub – replace with real data-source calls)
# ---------------------------------------------------------------------------

class Account(BaseModel):
    account_id: str
    email: str
    name: str
    balance: float


class CreditCard(BaseModel):
    card_id: str
    account_id: str
    card_number: str
    limit: float
    balance: float


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool(approval_mode="never_require")
def get_account(
    email: Annotated[str, Field(description="The user's email address.")],
) -> Account:
    """Get account information for a given user email."""
    # Stub implementation – replace with real data-source logic
    return Account(
        account_id="ACC-001",
        email=email,
        name="John Doe",
        balance=1500.00,
    )


@tool(approval_mode="never_require")
def get_credit_cards(
    account_id: Annotated[str, Field(description="The account ID to retrieve credit cards for.")],
) -> list[CreditCard]:
    """Get all credit cards associated with a given account ID."""
    # Stub implementation – replace with real data-source logic
    return [
        CreditCard(
            card_id="CC-001",
            account_id=account_id,
            card_number="**** **** **** 1234",
            limit=5000.00,
            balance=250.00,
        ),
        CreditCard(
            card_id="CC-002",
            account_id=account_id,
            card_number="**** **** **** 5678",
            limit=10000.00,
            balance=1200.00,
        ),
    ]


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class AccountAgent:
    instructions = """
You are a home banking assistant providing information about account balances
and credit cards. Use the available tools to look up account information and
credit card details for the user.
    """
    name = "AccountAgent"
    description = (
        "A home banking assistant that provides information about account "
        "balances and credit cards."
    )

    def __init__(self, client: AzureOpenAIChatClient):
        self.client = client

    async def build_agent(self) -> Agent:
        return Agent(
            client=self.client,
            instructions=AccountAgent.instructions.strip(),
            name=AccountAgent.name,
            tools=[get_account, get_credit_cards],
        )
