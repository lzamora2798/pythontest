from api.app import create_app
import pytest


@pytest.fixture
def client():
    """
    Flask test client.
    """
    app = create_app()
    with app.test_client() as client:
        yield client
