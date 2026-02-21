# Orchestrator - Handoff Strategy
# Agents pass control to each other based on conditions

from app.agent.account import Agent as AccountAgent
from app.agent.payment import Agent as PaymentAgent


class Orchestrator:
    def __init__(self):
        self.account_agent = AccountAgent("account")
        self.payment_agent = PaymentAgent("payment")
        self.current_agent = None

    def orchestrate(self, input_data):
        """
        Handoff orchestration: Routes input to appropriate agent,
        then passes result to next agent based on output.
        """
        # Start with account agent
        result = self.account_agent.act(input_data)
        
        # Handoff to payment agent if account processing succeeded
        if "received" in result:
            result = self.payment_agent.act(result)
        
        return result
