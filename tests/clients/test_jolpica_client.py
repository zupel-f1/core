from urllib.parse import urlencode
from app.clients.jolpica_client import fetch_from_jolpica

def test_fetch_from_jolpica(requests_mock):
    endpoint = "2023/drivers"
    params = {"limit" : 2}
    query_string = urlencode(params)
    url = f"https://api.jolpi.ca/ergast/f1/{endpoint}?{query_string}"
    
    # Mocked response
    mock_data = {
        "MRData": {
            "xmlns": "",
            "series": "f1",
            "url": "https://api.jolpi.ca/ergast/f1/2023/drivers/",
            "limit": "2",
            "offset": "0",
            "total": "22",
            "DriverTable": {
                "season": "2023",
                "Drivers": [
                    {
                        "driverId": "albon",
                        "permanentNumber": "23",
                        "code": "ALB",
                        "url": "http://en.wikipedia.org/wiki/Alexander_Albon",
                        "givenName": "Alexander",
                        "familyName": "Albon",
                        "dateOfBirth": "1996-03-23",
                        "nationality": "Thai"
                    },
                    {
                        "driverId": "alonso",
                        "permanentNumber": "14",
                        "code": "ALO",
                        "url": "http://en.wikipedia.org/wiki/Fernando_Alonso",
                        "givenName": "Fernando",
                        "familyName": "Alonso",
                        "dateOfBirth": "1981-07-29",
                        "nationality": "Spanish"
                    }
                ]
            }
        }
    }

    requests_mock.get(url, json=mock_data)

    response = fetch_from_jolpica(endpoint, params)

    assert "DriverTable" in response["MRData"]
    assert response["MRData"]["DriverTable"]["Drivers"][0]["driverId"] == "albon"
    