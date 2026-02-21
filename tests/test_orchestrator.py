"""Tests for the Orchestrator (Handoff strategy).

These tests exercise the full handoff workflow end-to-end using the real
AzureOpenAIChatClient configured via the DI container.  Make sure the
following environment variables are set before running:
    AZURE_OPENAI_ENDPOINT
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
and that `az login` has been completed (AzureCliCredential is used).
"""

import pytest

from agent_framework import WorkflowEvent
from app.config.di_container import Container


class TestOrchestrator:

    async def test_workflow_is_built_and_cached(self) -> None:
        """Calling _build_workflow twice should return the same object."""
        container = Container()
        orchestrator = container.orchestrator()

        wf1 = await orchestrator._build_workflow()
        wf2 = await orchestrator._build_workflow()

        assert wf1 is wf2, "Workflow should be lazily built and cached"

    async def test_general_query_streams_output_events(self) -> None:
        """A general question should be answered by the coordinator without
        triggering a handoff to AccountAgent."""
        container = Container()
        orchestrator = container.orchestrator()

        events: list[WorkflowEvent] = []
        async for event in orchestrator.processMessageStream(
            user_message="What is the capital of France?",
            thread_id="test-general-1",
        ):
            events.append(event)
            print(f"Event: type={event.type} executor={event.executor_id}")

        assert len(events) > 0, "Expected at least one event to be streamed"

        output_events = [e for e in events if e.type == "output"]
        assert len(output_events) > 0, "Expected at least one output event"

        # For a general question the coordinator should answer directly;
        # no handoff to AccountAgent is expected.
        handoff_events = [e for e in events if e.type == "handoff_sent"]
        account_handoffs = [
            e for e in handoff_events
            if hasattr(e, "data") and e.data and "Account" in str(getattr(e.data, "target", ""))
        ]
        assert len(account_handoffs) == 0, (
            "Did not expect the coordinator to hand off for a general query"
        )

    async def test_account_query_triggers_handoff_to_account_agent(self) -> None:
        """An account-balance question should cause the coordinator to hand
        off to AccountAgent and return account information."""
        container = Container()
        orchestrator = container.orchestrator()

        events: list[WorkflowEvent] = []
        async for event in orchestrator.processMessageStream(
            user_message="What is my account balance for user@example.com?",
            thread_id="test-account-1",
        ):
            events.append(event)
            print(f"Event: type={event.type} executor={event.executor_id}")

        assert len(events) > 0, "Expected at least one event to be streamed"

        # A handoff_sent event should appear, indicating the coordinator
        # transferred control to AccountAgent.
        handoff_events = [e for e in events if e.type == "handoff_sent"]
        assert len(handoff_events) > 0, (
            "Expected a handoff_sent event when asking about account balance"
        )

        # There should be output events produced by AccountAgent
        output_events = [e for e in events if e.type == "output"]
        assert len(output_events) > 0, "Expected output events from AccountAgent"

    async def test_credit_card_query_triggers_handoff_to_account_agent(self) -> None:
        """A credit-card question should also route to AccountAgent."""
        container = Container()
        orchestrator = container.orchestrator()

        events: list[WorkflowEvent] = []
        async for event in orchestrator.processMessageStream(
            user_message="Show me the credit cards for account ACC-001",
            thread_id="test-creditcard-1",
        ):
            events.append(event)
            print(f"Event: type={event.type} executor={event.executor_id}")

        assert len(events) > 0

        handoff_events = [e for e in events if e.type == "handoff_sent"]
        assert len(handoff_events) > 0, (
            "Expected a handoff_sent event when asking about credit cards"
        )
