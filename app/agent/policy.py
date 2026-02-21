import asyncio
import os
from typing import Annotated

from agent_framework import tool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from pydantic import Field

# Load environment variables from .env file
load_dotenv()


# Define the retrieve-policy tool
@tool(approval_mode="never_require")
def retrieve_policy(
    policy_name: Annotated[str, Field(description="The name of the policy to retrieve.")],
    policy_id: Annotated[str, Field(description="The ID of the policy to retrieve.")],
) -> str:
    """Retrieve a policy by name and ID."""
    return f"Policy '{policy_name}' (ID: {policy_id}) retrieved successfully."


class Agent:
    """Policy Agent - An agent for policy-related tasks with retrieve tool."""

    def __init__(self, name: str = "PolicyAgent"):
        self.name = name
        self.client = None
        self.agent = None

    async def _initialize_client(self):
        """Initialize the Azure OpenAI client if not already done."""
        if self.client is None:
            credential = AzureCliCredential()
            self.client = AzureOpenAIResponsesClient(
                project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
                deployment_name=os.environ["AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"],
                credential=credential,
            )
            self.agent = self.client.as_agent(
                name=self.name,
                instructions="You are a policy assistant. Use the retrieve_policy tool to fetch policies. Provide clear and concise policy guidance.",
                tools=retrieve_policy,
            )

    async def run(self, input_data: str, stream: bool = False):
        """Run the policy agent with the given input."""
        await self._initialize_client()
        if stream:
            return self.agent.run(input_data, stream=True)
        else:
            return await self.agent.run(input_data)

    def act(self, input_data):
        """Synchronous method for policy agent logic."""
        return f"Agent {self.name} received: {input_data}"
