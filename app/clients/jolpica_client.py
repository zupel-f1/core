import requests


def fetch_from_jolpica(endpoint: str, params: dict | None = None):
    base_url = "https://api.jolpi.ca/ergast/f1"
    endpoint = f"{base_url}/{endpoint}"
    initial_response = requests.get(endpoint, params=params)
    initial_response.raise_for_status()
    response = initial_response.json()
    return response

