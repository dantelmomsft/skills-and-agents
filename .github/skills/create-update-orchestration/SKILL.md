---
name: create-update-orchestration
description: customize your code base update the agent orchestration logic
---

1. read the list of agents in app/agents folder and present to the user the list.
2. read app/agents/orchestrator.py to check the current orchestration strategy and check all agents are included. if app/agents/orchestrator.py is not present create it.
3. Explain the user the current orchestration strategy and ask what are the other available options.
4. based on user's input update the app/agents/orchestrator.py to implement the new orchestration strategy.
5. create an orchestrator test case in tests folder to test the orchestration logic.
6. run the test case to make sure the orchestration logic is working as expected.

# Orchestration strategies
- Sequential
- Fan-in, Fan-out
- Handoff
- Magentic

# Code Generation Guidelines
- For sequential orchestration use code samples list in references/sequential.md
- For Handoff orchestration use code samples list in references/handoff.md
- For Magentic orchestration use code samples list in references/magentic.md