from typing import AsyncGenerator
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import WorkflowEvent
from agent_framework.orchestrations import HandoffBuilder
from app.agents.sample_agent import SampleAgent
from app.agents.account_agent import AccountAgent

import logging

logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrates SampleAgent and AccountAgent using a Handoff strategy.

    SampleAgent acts as the coordinator / triage agent.  It handles general
    queries and hands off to AccountAgent whenever the user asks about account
    balances or credit cards.
    """

    _coordinator_instructions = """
You are a helpful customer-support coordinator.
Answer general questions directly.
If the user asks about account balances, credit card details, or any other
banking information, hand off to the AccountAgent specialist.
"""

    def __init__(
        self,
        client: AzureOpenAIChatClient,
        sample_agent: SampleAgent,
        account_agent: AccountAgent,
    ):
        self.client = client
        self.sample_agent = sample_agent
        self.account_agent = account_agent
        self.workflow = None  # Will be initialized lazily on first use

    async def _build_workflow(self):
        """Build the HandoffBuilder workflow (lazy, cached)."""
        if self.workflow is not None:
            return self.workflow

        # Build the two agents
        coordinator = await self.sample_agent.build_agent()
        account = await self.account_agent.build_agent()

        # Override coordinator instructions to include routing guidance
        coordinator.instructions = self._coordinator_instructions.strip()

        # Assemble the handoff workflow
        self.workflow = (
            HandoffBuilder(
                name="banking_support_handoff",
                participants=[coordinator, account],
            )
            .with_start_agent(coordinator)
            .build()
        )
        logger.info("Handoff workflow built with coordinator=%s, specialist=%s",
                    coordinator.name, account.name)
        return self.workflow

    async def processMessageStream(
        self, user_message: str, thread_id: str
    ) -> AsyncGenerator[WorkflowEvent, None]:
        """Stream WorkflowEvents for a single user turn.

        The coordinator agent handles the message first.  If it decides to
        hand off to AccountAgent, the framework automatically invokes the
        specialist and the corresponding events are yielded here.
        """
        workflow = await self._build_workflow()
        async for event in workflow.run(user_message, stream=True):
            logger.debug("Event: type=%s executor=%s", event.type, event.executor_id)
            yield event