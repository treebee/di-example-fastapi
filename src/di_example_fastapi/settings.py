import enum
from typing import Optional
from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageBackendEnum(str, enum.Enum):
    factory = "factory"
    postgres = "postgres"
    redis = "redis"


class Settings(BaseSettings):
    debug: bool = False
    storage_backend: StorageBackendEnum = StorageBackendEnum.factory
    redis_url: Optional[RedisDsn] = None
    postgres_url: Optional[PostgresDsn] = None

    @model_validator(mode="before")
    def redis_url_validator(cls, data):
        if data["storage_backend"] == StorageBackendEnum.redis and data.get("redis_url") is None:
            raise ValueError("Redis URL is required for Redis storage backend")
        return data

    @model_validator(mode="before")
    def postgres_url_validator(cls, data):
        if (
            data["storage_backend"] == StorageBackendEnum.postgres
            and data.get("postgres_url") is None
        ):
            raise ValueError("Postgres URL is required for Postgres storage backend")
        return data

    model_config = SettingsConfigDict(frozen=True)
