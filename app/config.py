from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    BATCH_SIZE: int = 1000

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")


settings = Settings()
