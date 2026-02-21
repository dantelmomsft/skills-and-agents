---
name: create-update-orchestration
description: customize your code base update the agent orchestration logic
---

1. read the list of agents in app/agent folder and present to the user the list. an agent file look like name-agent.py
2. read app/agent/orchestrator.py to check the current orchestration strategy and check all agents are included. if app/agent/orchestrator is not present create it.
3. Explain the user the current orchestration strategy and ask what are the other available options.


# Orchestration strategies
- Sequential
- Fan-in, Fan-out
- Handoff
- Magentic