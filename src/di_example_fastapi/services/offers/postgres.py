from sqlalchemy.orm import Session
from di_example_fastapi import models, schemas

from di_example_fastapi.services.offers.base import OfferService


class PostgresOfferService(OfferService):
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get(self, id: int) -> schemas.Offer | None:
        offer = self._db_session.query(models.Offer).get(id)
        if offer:
            return schemas.Offer.model_validate(offer)
        return None

    def list(self) -> list[schemas.Offer]:
        return [schemas.Offer.model_validate(o) for o in self._db_session.query(models.Offer).all()]

    def create(self, offer: schemas.OfferCreate) -> schemas.Offer:
        offer = models.Offer(**offer.model_dump())
        self._db_session.add(offer)
        self._db_session.commit()
        return schemas.Offer.model_validate(offer)
