import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Offer(Base):
    __tablename__ = "offers"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text)
    description = sa.Column(sa.Text)
    price = sa.Column(sa.Numeric(18, 2))
