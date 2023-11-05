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


@pytest.fixture
def mock_measures():
    return {
        "this": "succeeded",
        "by": "getting",
        "the": "sweets",
        "with": [
            {
                "thing": "thecore",
                "created": "2023-11-05T01:37:56.840Z",
                "content": {
                    "temperature": 24.4,
                    "humidity": 56,
                    "temperature2": 19.1,
                    "humidity2": 49,
                    "temperature3": 20.3,
                    "humidity3": 48,
                    "temperature4": "nan",
                    "humidity4": 0,
                    "temperature5": -127,
                    "temperature6": -127,
                    "VWC": 60.29,
                    "lux": -1,
                    "tensio": 353,
                    "R1": 1,
                    "R2": 0,
                    "R3": 0,
                    "R4": 0,
                    "R5": 0,
                    "R6": 0,
                    "R7": 0,
                    "L8": 1
                }
            }
        ]
    }

