from agent_framework import Agent, FunctionTool


def retrieve_account(user_mail: str) -> dict:
    """
    Retrieve an account object by user email.
    
    Args:
        user_mail: The email address of the user
        
    Returns:
        Account object containing user details
    """
    # Mock implementation - in production, this would query a database
    return {
        "user_mail": user_mail,
        "account_id": f"ACC_{hash(user_mail) % 10000}",
        "status": "active",
        "balance": 1000.00,
        "created_date": "2025-01-01"
    }


class Agent:
    def __init__(self, name: str):
        self.name = name
        self.agent = Agent(
            name=name,
            tools=[
                FunctionTool(
                    retrieve_account,
                    description="Retrieve account details by user email address"
                )
            ]
        )
    
    def act(self, input_data):
        """Process input through the agent"""
        return self.agent.act(input_data)
