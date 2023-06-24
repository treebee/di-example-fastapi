import functools
from typing import Annotated
from fastapi import Depends
import redis
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

from .settings import Settings, StorageBackendEnum
from .models import Base
from .services.offers import (
    FactoryOfferService,
    OfferService,
    PostgresOfferService,
    RedisOfferService,
)


@functools.lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings


@functools.lru_cache
def get_session_factory(settings: Settings) -> sessionmaker[Session]:
    if settings.postgres_url is None:
        raise ValueError("Postgres URL not configured")

    engine = sa.create_engine(str(settings.postgres_url))
    Base.metadata.create_all(engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_redis_offer_service(settings: Settings) -> RedisOfferService:
    if settings.redis_url is None:
        raise ValueError("Redis URL not configured")
    with redis.from_url(str(settings.redis_url)) as client:
        yield RedisOfferService(client)


def create_postgres_offer_service(settings: Settings) -> PostgresOfferService:
    session_factory = get_session_factory(settings)
    session = session_factory()
    try:
        yield PostgresOfferService(session)
    finally:
        session.close()


def get_offer_service(settings: Annotated[Settings, Depends(get_settings)]) -> OfferService:
    if settings.storage_backend == StorageBackendEnum.redis:
        yield from create_redis_offer_service(settings)
    elif settings.storage_backend == StorageBackendEnum.postgres:
        yield from create_postgres_offer_service(settings)
    elif settings.storage_backend == StorageBackendEnum.factory:
        yield FactoryOfferService()
    else:
        raise NotImplementedError(f"Storage backend {settings.storage_backend} not implemented")
