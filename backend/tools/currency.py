import os
from dotenv import load_dotenv
import requests
import math

load_dotenv()

def get_currency(amount, from_currency,to_currency):
    api_key = os.environ.get("CURRENCY_EXCHANGE_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    try:
        response = requests.get(url)
        data = response.json()
        result = data.get('conversion_rates')
        return f"Converted {amount} {from_currency} to {math.floor(result[to_currency]*amount)} {to_currency}"
    except:
        return f"Unable to convert currency from {from_currency} to {to_currency}"