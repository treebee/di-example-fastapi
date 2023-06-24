import abc
from typing import Optional, List

from polyfactory.factories.pydantic_factory import ModelFactory

from ...schemas import Offer, OfferCreate


class OfferService(abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> Optional[Offer]:
        ...

    @abc.abstractmethod
    def list(self) -> List[Offer]:
        ...

    @abc.abstractmethod
    def create(self, offer: OfferCreate) -> Offer:
        ...


__all__ = ("OfferService",)
