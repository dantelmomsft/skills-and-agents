---
name: create-update-agent
description: customize your code base and create/update a new agent
---

1. ask the name of the agent
2. ask agent instructions 
3. ask if any tools need to be added
4. create {agent}.py in agents folder
5. register the agent class in the di_container.py
6. if orchestrator.py is present check if the new agent need to be added to the orchestration flow, if yes update the orchestration flow to include the new agent.
7. add a test case in tests folder to test the new agent.
8. run the test case to make sure the new agent is working as expected.

# Code Generation Guidelines
- For plain agent creation use code samples list in references/agent.md
- For adding tools to agent use code samples list in references/tools.md
- For adding context provider to agent use code samples list in references/context.md