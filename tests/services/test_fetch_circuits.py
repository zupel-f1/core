import pytest
from unittest.mock import patch

from app.services import fetch_circuits

@pytest.fixture
def sample_circuit_data():
    return [
        {
            "circuitId": "albert_park",
            "url": "https://en.wikipedia.org/wiki/Albert_Park_Circuit",
            "circuitName": "Albert Park Grand Prix Circuit",
            "Location": {
                "lat": "-37.8497",
                "long": "144.968",
                "locality": "Melbourne",
                "country": "Australia"
            }
        }
    ]

@patch("app.services.fetch_circuits.fetch_from_jolpica")
def test_fetch_circuits_from_jolpica(mock_fetch):
    mock_fetch.side_effect = [
        {
            "MRData": {
                "CircuitTable": {
                    "Circuits": [
                        {
                            "circuitId": "catalunya", 
                            "url": "url", 
                            "circuitName": "Circuit de Barcelona-Catalunya", 
                            "Location": {
                                "lat": "41.57",
                                "long": "2.26111",
                                "locality": "Montmeló",
                                "country": "Spain"
                            }
                        }
                    ]
                }
            }
        },
        {
            "MRData": {
                "CircuitTable": {
                    "Circuits": []
                }
            }
        }
    ]
    circuits = fetch_circuits._fetch_circuits_from_jolpica()
    assert len(circuits) == 1
    assert circuits[0]["circuitId"] == "catalunya"

def test_transform_circuits_data(sample_circuit_data):
    transformed = fetch_circuits._transform_circuits_data(sample_circuit_data)
    assert transformed == [{
        "external_id": "albert_park",
        "url": "https://en.wikipedia.org/wiki/Albert_Park_Circuit",
        "circuit_name": "Albert Park Grand Prix Circuit",
        "city": "Melbourne",
        "country": "Australia"
    }]

@patch("app.services.fetch_circuits.Circuit")
@patch("app.services.fetch_circuits.db")
def test_update_database_circuits(mock_db, mock_circuit, sample_circuit_data):
    mock_db.session.query.return_value.filter.return_value.one_or_none.return_value = None
    circuits = fetch_circuits._transform_circuits_data(sample_circuit_data)
    fetch_circuits._update_database_circuits(circuits)
    assert mock_db.session.add.call_count == 1
    assert mock_db.session.commit.call_count == 1