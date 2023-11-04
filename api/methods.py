import requests
import os

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


def save_to_db(exchange_data):
    with db_connection():
        Currency.objects.create(**exchange_data)

def push_to_webhook(data):
    webhook_url = os.environ["WEBSOCKED_URL"]
    webhook_id = os.environ["WEBSOCKED_ID"]
    data = requests.post(f"{webhook_url}/{webhook_id}", json=data)

def query_to_currency_page(data):
    url = os.environ["CURRENCY_URL"]
    try:
        bearer_token = get_bearer_token(url)

        from_currency = data["from_currency"]
        to_currency = data["to_currency"]
        amount = data["amount"]
        get_url = f"{url}/ofxrates/{from_currency}/{to_currency}/{amount}"

        headers = {"Authorization": f"Bearer {bearer_token}"}
        exchange_data = requests.get(get_url, headers=headers)

        data["convert_value"] = exchange_data.json()["convertedAmount"]
        save_to_db(data)
        push_to_webhook(data)

        return data

    except Exception as err:
        print(err)
        return err

