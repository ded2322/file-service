from pathlib import Path
from typing import Literal

import environ
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(BASE_DIR / ".env")


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    ACCESS_KEY: str
    SECRET_KEY: str
    ENDPOINT_URL: str
    BUCKET_NAME: str

    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{env('TEST_DB_USER')}:{env('TEST_DB_PASSWORD')}@{env('TEST_DB_HOST')}:{env('TEST_DB_PORT')}/{env('TEST_DB_NAME')}"

    model_config = SettingsConfigDict(env_file=".env_non_dev")


class FilePath:
    BASE_UPLOAD_DIR: Path = Path("/core/static")
    TEXT_UPLOAD_DIR: str = BASE_UPLOAD_DIR / "txt_files"
    IMAGE_UPLOAD_DIR: str = BASE_UPLOAD_DIR / "images_files"
    VIDEO_UPLOAD_DIR: str = BASE_UPLOAD_DIR / "media_files"
    OTHER_UPLOAD_DIR: str = BASE_UPLOAD_DIR / "other_files"


settings = Settings()
files_paths = FilePath()
