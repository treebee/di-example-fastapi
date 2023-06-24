from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_offer_service
from ..schemas import Offer, OfferCreate
from ..services.offers import OfferService

router = APIRouter(prefix="/offers", tags=["offers"])


@router.get("/")
def list_offers(offer_service: Annotated[OfferService, Depends(get_offer_service)]) -> List[Offer]:
    return offer_service.list()


@router.get("/{id}")
def get_offer(
    id: int, offer_service: Annotated[OfferService, Depends(get_offer_service)]
) -> Offer | None:
    if (offer := offer_service.get(id)) is None:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@router.post("/")
def create_offer(
    offer_service: Annotated[OfferService, Depends(get_offer_service)], offer: OfferCreate
) -> Offer:
    return offer_service.create(offer)
