import pytest
from fastapi.testclient import TestClient

from di_example_fastapi.app import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
