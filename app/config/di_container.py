"""Dependency injection container configuration."""

import os
from dependency_injector import containers, providers
from app.config.azure_credential import get_azure_credential
from app.config.settings import settings
from app.agents.sample_agent import SampleAgent
from app.agents.account_agent import AccountAgent
from app.agents.orchestrator import Orchestrator

from agent_framework.azure import AzureOpenAIChatClient



class Container(containers.DeclarativeContainer):
    """IoC container for application dependencies."""
   

    # Azure Chat based agents. Unfortunately we can't create reusable singleton instance of AzureOpenAiChatCLient as it does not support token expiration management.
    _azure_chat_client = providers.Factory(
        AzureOpenAIChatClient,
        credential=providers.Factory(get_azure_credential), 
        endpoint=settings.AZURE_OPENAI_ENDPOINT,deployment_name=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
    )

    # Sample Agent
    sample_agent = providers.Factory(
    SampleAgent,
    client=_azure_chat_client
    )

    # Account Agent
    account_agent = providers.Factory(
        AccountAgent,
        client=_azure_chat_client
    )

    # Orchestrator
    orchestrator = providers.Factory(
        Orchestrator,
        client=_azure_chat_client,
        sample_agent=sample_agent,
        account_agent=account_agent
    )


   
   