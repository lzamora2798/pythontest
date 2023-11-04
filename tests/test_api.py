import json


class TestApi:
    def test_convert_currency(self, client):
        """Test if get method works."""

        url = f"/convertCurrency"
        data= {
            "from_currency": "USD",
            "to_currency": "EUR",
            "amount": "1"
        }
        response = client.post(url, json=data)
        data = json.loads(response.data)
        assert response.status_code == 200

