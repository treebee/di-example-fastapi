import pytest
from fastapi.testclient import TestClient

from di_example_fastapi.schemas import Offer
from di_example_fastapi.services.offers import FactoryOfferService
from di_example_fastapi.dependencies import get_offer_service


class DummyOfferService(FactoryOfferService):
    def __init__(self):
        self._offers = {
            1: Offer(id=1, title="Offer 1", description="Description 1", price="10.0"),
            2: Offer(id=2, title="Offer 2", description="Description 2", price="20.0"),
            3: Offer(id=3, title="Offer 3", description="Description 3", price="30.0"),
        }


@pytest.fixture(scope="module")
def client():
    from di_example_fastapi.app import app

    app.dependency_overrides[get_offer_service] = lambda: DummyOfferService()
    with TestClient(app) as c:
        yield c


def test_list_offers(client):
    response = client.get("/offers/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Offer 1", "description": "Description 1", "price": '10.0'},
        {"id": 2, "title": "Offer 2", "description": "Description 2", "price": '20.0'},
        {"id": 3, "title": "Offer 3", "description": "Description 3", "price": '30.0'},
    ]


@pytest.mark.parametrize(
    "id,expected_status_code,expected_response",
    [
        (1, 200, {"id": 1, "title": "Offer 1", "description": "Description 1", "price": "10.0"}),
        (404, 404, {"detail": "Offer not found"}),
    ],
)
def test_get_offer(client, id, expected_status_code, expected_response):
    response = client.get(f"/offers/{id}")
    assert response.status_code == expected_status_code
    assert response.json() == expected_response


def test_create_offer(client):
    response = client.post(
        "/offers/", json={"title": "Offer 4", "description": "Description 4", "price": "40.0"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 4,
        "title": "Offer 4",
        "description": "Description 4",
        "price": "40.0",
    }
