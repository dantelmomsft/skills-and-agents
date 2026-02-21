import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_files() -> List[str]:
    """Get list of environment files to load based on current environment."""
    env = os.getenv("PROFILE")

    if env:
        print(f"Loading environment files for environment: {env}")
    else:
        print("No environment specified, environment variables only configuration will be used.")
        return []
    
    env = env.lower()
    # List of env files to try (in order of priority - later files override earlier ones)
    env_files = [
        ".env",  # Base environment file
        f".env.{env}"  # Environment-specific file
        
    ]

    final_env_files = []
    # print found env files only if path exists
    print("Environment files loading:")    
    for f in env_files:
        print(f"Loading: {f}")
        if os.path.exists(f):
            final_env_files.append(f)
            print(f"{f} Loaded")

    return final_env_files

class Settings(BaseSettings):
    """Application settings loaded from environment or environment-specific .env files.

    Settings are loaded in the following order (later sources override earlier ones):
    1. Default values defined in the class
    2. Environment variables
    3. Base .env file
    4. Environment-specific .env file (e.g., .env.development, .env.production)
    
    The environment is determined by the ENVIRONMENT environment variable or defaults to 'development'.
    """

    # app-level
    APP_NAME: str = "My App"
    PROFILE: str = Field(default="prod")

    #Logging and monitoring
    APPLICATIONINSIGHTS_CONNECTION_STRING: str | None = Field(default=None)
    ENABLE_OTEL : bool = Field(default=True)
  
    
    #Azure OpenAI Chat configuration
    AZURE_OPENAI_ENDPOINT: str | None = Field(default=None)
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: str = Field(default="gpt-4o")


    model_config = SettingsConfigDict(
        env_file=get_env_files(),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()