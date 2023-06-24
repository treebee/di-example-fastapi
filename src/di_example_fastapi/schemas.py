from typing import Optional
from pydantic import ConfigDict, BaseModel, condecimal


class OfferCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: condecimal(decimal_places=2)  # type: ignore


class Offer(OfferCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
