"""Tests for SampleAgent."""

import pytest

from app.config.di_container import Container


class TestSampleAgent:

    async def test_build_agent_and_run(self) -> None:
        """Build SampleAgent via the DI container and call the real LLM."""
        container = Container()

        sample_agent = container.sample_agent()
        agent = await sample_agent.build_agent()

        result = await agent.run("What is the capital of France?")
        print(f"Agent: {result}")

        assert result is not None
