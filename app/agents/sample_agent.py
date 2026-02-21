from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import Agent, MCPStreamableHTTPTool
import logging

logger = logging.getLogger(__name__)

class SampleAgent :
    instructions = """
you are an helpful assistant
        """
    name = "SampleAgent"
    description = "This is a sample agent that demonstrates how to build an Agent with Azure OpenAI Chat client and custom tools."

    def __init__(self, client: AzureOpenAIChatClient):
        self.client = client
        

    async def build_agent(self) -> Agent:
    
      return Agent(
      client=self.client,
      instructions=SampleAgent.instructions.strip(),
      name=SampleAgent.name)
            
        