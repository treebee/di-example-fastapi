from typing import List

from polyfactory.factories.pydantic_factory import ModelFactory

from di_example_fastapi import schemas
from di_example_fastapi.services.offers.base import OfferService


class OfferFactory(ModelFactory):
    __model__ = schemas.Offer


class FactoryOfferService(OfferService):
    """Implementation of the OffersService interface that randomly generates
    data via polyfactory. Only useful for development and testing.
    """

    def __init__(self):
        self._offers = {offer_id: OfferFactory.build(id=offer_id) for offer_id in range(1, 11)}

    def get(self, id: int) -> schemas.Offer | None:
        return self._offers.get(id)

    def list(self) -> List[schemas.Offer]:
        return list(self._offers.values())

    def create(self, offer: schemas.OfferCreate) -> schemas.Offer:
        offer_id = max(self._offers.keys()) + 1
        offer = schemas.Offer(id=offer_id, **offer.model_dump())
        self._offers[offer_id] = offer
        return offer
