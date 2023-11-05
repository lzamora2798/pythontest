import json
from unittest import mock
from api.crontask import run
import requests

class TestApi:
    @mock.patch("api.methods.get_exchange_value")
    @mock.patch("api.methods.get_bearer_token")
    @mock.patch("api.methods.push_to_webhook")
    def test_convert_currency(self, mock_bearer_token, mock_exchange_value, mock_webhook, client):
        """Test if post method works."""

        url = f"/convertCurrency"
        data = {
            "from_currency": "USD",
            "to_currency": "EUR",
            "amount": "1"
        }

        mock_bearer_token.return_value = "fake bearer token"
        mock_exchange_value.return_value = 1.0
        mock_webhook.return_value = None

        response = client.post(url, json=data)
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data["success"]

    @mock.patch("api.methods.invoke_lambda_")
    def test_cron_task_request(self, invoke_lambda, client):

        """Test if get method works."""
        invoke_lambda.return_value = {"msg": "ok"}
        url = f"/saveMeasure"
        response = client.get(url)
        data = json.loads(response.data)
        assert data

    @mock.patch("api.crontask.requests.get")
    def test_cron_task(self, mock_get, mock_measures):
        response = requests.Response()
        response._content = str.encode(json.dumps(mock_measures))
        mock_get.return_value.status_code = 200
        mock_get.return_value = response
        c = run([], [])
        assert c
