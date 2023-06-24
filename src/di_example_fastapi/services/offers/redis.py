import redis

from di_example_fastapi import schemas
from di_example_fastapi.services.offers.base import OfferService


class RedisOfferService(OfferService):
    def __init__(self, client: redis.Redis):
        self._client = client

    def get(self, id: int) -> schemas.Offer | None:
        offer = self._client.get(f"offer:{id}")
        if offer:
            return schemas.Offer.model_validate_json(offer)
        return None

    def list(self) -> list[schemas.Offer]:
        keys = self._client.keys("offer:*")
        return [
            schemas.Offer.model_validate_json(offer)
            for offer in [self._client.get(key) for key in keys]
            if offer is not None
        ]

    def create(self, offer: schemas.OfferCreate) -> schemas.Offer:
        offer_id = self._client.incr("offer_id")
        offer = schemas.Offer(id=offer_id, **offer.model_dump())
        self._client.set(f"offer:{offer_id}", offer.model_dump_json())
        return offer
