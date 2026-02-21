---
name: app-init
description: Init the code base from scratch with a basic agent app
---

1. run ```bash
python download_folder.py pragma81/agent-python-kb app-shell --branch main --output .
```
2. create the .env.dev file based on env.dev.example and store it in the app folder.
3. ask the user to provide the values for properties in .env.dev file, and fill in the values in .env.dev file.
4. copy the content of .env.dev to tests/.env file and add a property PROFILE=dev.
5. run the test_sample_agent.py making sure tests/.env file is used to make sure the app setup is successful.