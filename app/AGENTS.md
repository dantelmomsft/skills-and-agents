# Agent App Shell

This is a Python project scaffold for building AI agent applications using the `agent-framework` library with Azure OpenAI as the backend.

---

## Directory Structure

```
├── app/                        # Main application package
│   ├── AGENTS.md               # This file – project structure and developer guide
│   ├── main.py                 # Application entry point
│   ├── .env.dev.example        # Example env file for local development
│   ├── .env.dev                # Local dev env file (not committed)
│   ├── agents/                 # Agent definitions
│   │   ├── orchestrator.py     # Orchestrator that routes messages to agents
│   │   └── sample_agent.py     # Example agent built on AzureOpenAIChatClient
│   ├── config/                 # Configuration and infrastructure wiring
│   │   ├── settings.py         # Pydantic-based settings loaded from env/env files
│   │   ├── azure_credential.py # Azure credential factory (CLI vs Managed Identity)
│   │   ├── di_container.py     # Dependency injection container (dependency-injector)
│   │   └── logging.py          # Logging setup with optional OpenTelemetry integration
│   └── tools/                  # Custom agent tools (empty – add MCP or function tools here)
├── tests/                      # Test suite
│   ├── .env                    # Test-specific env vars (loaded automatically by pytest-dotenv)
│   ├── __init__.py
│   └── test_sample_agent.py    # Integration test: builds SampleAgent via DI and calls the LLM
├── pyproject.toml              # Project metadata, dependencies, and pytest configuration
└── uv.lock                     # Locked dependency versions (managed by uv)
```

---

## Key Files

### `app/main.py`
Entry point. Initialises logging, builds the DI container, and starts the app.

### `app/config/settings.py`
Pydantic `BaseSettings` class. Loads values from environment variables and, if `PROFILE` is set, from `.env` and `.env.<PROFILE>` files in the current working directory. Key settings:

### `app/config/azure_credential.py`
Returns the appropriate Azure credential:
- `PROFILE=dev` → `AzureCliCredential` (uses `az login`)
- anything else → `ManagedIdentityCredential` (requires `AZURE_CLIENT_ID`)

### `app/config/di_container.py`
Wires together `AzureOpenAIChatClient`, `SampleAgent`, and `Orchestrator` using `dependency-injector` factory providers.

### `app/agents/sample_agent.py`
Minimal agent example. Builds an `Agent` from the framework with a system instruction and the configured chat client.

### `app/agents/orchestrator.py`
Routes user messages to agents. Currently a stub — implement `processMessageStream` to add real orchestration logic.

### `app/tools/`
Empty directory. Add custom MCP (`MCPStreamableHTTPTool`) or function tools here and wire them into your agents.

### `app/.env.dev.example`
Template for local developer `.env.dev` files. Copy to `.env.dev`, fill in your values, and set `PROFILE=dev`.

---

## Running Tests

### Prerequisites

1. **Install dependencies** (first time, or after changes to `pyproject.toml`):
   ```bash
   uv sync --extra dev
   ```

2. **Fill in test credentials** — edit `tests/.env` with your real Azure OpenAI endpoint:
   ```dotenv
   PROFILE=dev
   AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
   ENABLE_OTEL=False
   ```

3. **Log in to Azure CLI** (required when `PROFILE=dev`):
   ```bash
   az login
   ```

### Run Tests

```bash
uv run python -m pytest tests/ -v
```

> **Why `python -m pytest` instead of `uv run pytest`?**  
> `uv run pytest` may resolve to the system-installed pytest instead of the one in the project's `.venv`. Using `python -m pytest` ensures the correct virtual environment is used.

`pytest-dotenv` (configured in `pyproject.toml`) automatically loads `tests/.env` before any test modules are imported, so `Settings` and the DI container are initialised with the test values.

