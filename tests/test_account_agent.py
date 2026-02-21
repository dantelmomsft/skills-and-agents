"""Tests for AccountAgent."""

import pytest

from app.config.di_container import Container


class TestAccountAgent:

    async def test_build_agent_and_run_account_balance(self) -> None:
        """Build AccountAgent via the DI container and ask about account balance."""
        container = Container()

        account_agent = container.account_agent()
        agent = await account_agent.build_agent()

        result = await agent.run("What is my account balance for user@example.com?")
        print(f"Agent: {result}")

        assert result is not None

    async def test_build_agent_and_run_credit_cards(self) -> None:
        """Build AccountAgent via the DI container and ask about credit cards."""
        container = Container()

        account_agent = container.account_agent()
        agent = await account_agent.build_agent()

        result = await agent.run("Show me the credit cards for account ACC-001")
        print(f"Agent: {result}")

        assert result is not None
