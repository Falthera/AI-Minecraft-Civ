from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Service
    host: str = "0.0.0.0"
    port: int = 8001
    api_key: str = "changeme"

    # Models
    fast_model_path: str = "/models/fast-model.gguf"
    main_model_path: str = "/models/main-model.gguf"
    fast_model_context_size: int = 2048
    main_model_context_size: int = 4096

    # Inference
    max_concurrency: int = 4
    request_timeout_seconds: int = 120
    max_queue_size: int = 500

    # Embeddings
    embedding_model_path: str = "/models/embedding-model.gguf"


settings = Settings()
