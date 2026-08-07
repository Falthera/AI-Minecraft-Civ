from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    host: str = "0.0.0.0"
    port: int = 8000
    api_key: str = "changeme"

    database_url: str = "postgresql://ai_civilization:changeme@postgres:5432/ai_civilization"
    minecraft_api_url: str = "http://minecraft:25565"
    minecraft_api_key: str = "changeme"
    inference_api_url: str = "http://inference:8001"
    inference_api_key: str = "changeme"

    max_agents: int = 10000
    scheduler_tick_seconds: float = 1.0


settings = Settings()
