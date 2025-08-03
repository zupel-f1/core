import pytest
from unittest.mock import patch

from app.services import fetch_drivers

@pytest.fixture
def sample_driver_data():
    return [
        {
            "driverId": "hamilton",
            "url": "http://example.com/hamilton",
            "givenName": "Lewis",
            "familyName": "Hamilton",
            "nationality": "British",
            "dateOfBirth": "1985-01-07",
            "code": "HAM",
            "permanentNumber": "44"
        }
    ]

def test_transform_drivers_data(sample_driver_data):
    transformed = fetch_drivers._transform_drivers_data(sample_driver_data)
    assert transformed == [{
        "external_id": "hamilton",
        "url": "http://example.com/hamilton",
        "given_name": "Lewis",
        "family_name": "Hamilton",
        "nationality": "British",
        "date_of_birth": "1985-01-07",
        "code": "HAM",
        "permanent_number": "44"
    }]

@patch("app.services.fetch_drivers.fetch_from_jolpica")
def test_fetch_drivers_from_jolpica(mock_fetch):
    mock_fetch.side_effect = [
        {
            "MRData": {
                "DriverTable": {
                    "Drivers": [
                        {"driverId": "hamilton", "url": "url", "givenName": "Lewis", "familyName": "Hamilton", "nationality": "British"}
                    ]
                }
            }
        },
        {
            "MRData": {
                "DriverTable": {
                    "Drivers": []
                }
            }
        }
    ]
    drivers = fetch_drivers._fetch_drivers_from_jolpica()
    assert len(drivers) == 1
    assert drivers[0]["driverId"] == "hamilton"

@patch("app.services.fetch_drivers.Driver")
@patch("app.services.fetch_drivers.db")
def test_update_database_drivers(mock_db, mock_driver, sample_driver_data):
    mock_driver.query.filter_by.return_value.one_or_none.return_value = None
    drivers = fetch_drivers._transform_drivers_data(sample_driver_data)
    fetch_drivers._update_database_drivers(drivers)
    assert mock_db.session.add.call_count == 1
    assert mock_db.session.commit.call_count == 1
