import requests
import os
import boto3

from db.connection import db_connection
from db.models import Currency


def get_bearer_token(url):
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'ofxrates',
        }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = requests.post(f"{url}/oauth/token", headers=headers, data=data)

    return data.json()["access_token"]


def get_exchange_value(bearer_token, url):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)
    return response.json()["convertedAmount"]


def push_to_webhook(data):
    webhook_url = os.environ["WEBSOCKED_URL"]
    webhook_id = os.environ["WEBSOCKED_ID"]
    requests.post(f"{webhook_url}/{webhook_id}", json=data)


def query_to_currency_page(data):
    url = os.environ["CURRENCY_URL"]
    try:
        bearer_token = get_bearer_token(url)

        from_currency = data["from_currency"]
        to_currency = data["to_currency"]
        amount = data["amount"]
        get_url = f"{url}/ofxrates/{from_currency}/{to_currency}/{amount}"

        data["convert_value"] = get_exchange_value(bearer_token, get_url)

        with db_connection():
            Currency.objects.create(**data)
            push_to_webhook(data)
            return {"success": True}

    except Exception as err:
        return {"success": False, "err": str(err)}


def invoke_lambda_():
    try:
        client = boto3.client("lambda", region_name='us-east-1')
        request = client.invoke(FunctionName="cronTask",
                                InvocationType='RequestResponse')
        return {"msg": "ok"}
    except Exception as err:
        return {"err": str(err)}

