# Account Agent class

class Agent:
    def __init__(self, name: str):
        self.name = name

    def act(self, input_data):
        """Account agent logic."""
        return f"Agent {self.name} received: {input_data}"
