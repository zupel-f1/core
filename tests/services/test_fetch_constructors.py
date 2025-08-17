from unittest.mock import patch

import pytest

from app.services import fetch_constructors


@pytest.fixture
def sample_constructor_data():
    return [
        {
            "constructorId": "alpine",
            "url": "http://en.wikipedia.org/wiki/Alpine_F1_Team",
            "name": "Alpine F1 Team",
            "nationality": "French"
        }
    ]


@patch("app.services.fetch_constructors.fetch_from_jolpica")
def test_fetch_constructors_from_jolpica(mock_fetch):
    mock_fetch.side_effect = [
        {
            "MRData": {
                "ConstructorTable": {
                    "Constructors": [
                        {"constructorId": "alpine",
                         "url": "http://en.wikipedia.org/wiki/Alpine_F1_Team",
                         "name": "Alpine F1 Team",
                         "nationality": "French"}
                    ]
                }
            }
        },
        {
            "MRData": {
                "ConstructorTable": {
                    "Constructors": []
                }
            }
        }
    ]
    constructors = fetch_constructors._fetch_constructors_from_jolpica()
    assert len(constructors) == 1
    assert constructors[0]["constructorId"] == "alpine"


def test_transform_constructors_data(sample_constructor_data):
    transformed = fetch_constructors._transform_constructors_data(sample_constructor_data)
    assert transformed == [{
        "external_id": "alpine",
        "url": "http://en.wikipedia.org/wiki/Alpine_F1_Team",
        "name": "Alpine F1 Team",
        "nationality": "French"
    }]


@patch("app.services.fetch_constructors.Constructor")
@patch("app.services.fetch_constructors.db")
def test_update_database_drivers(mock_db, mock_constructor, sample_constructor_data):
    mock_constructor.query.filter_by.return_value.one_or_none.return_value = None
    constructors = fetch_constructors._transform_constructors_data(sample_constructor_data)
    fetch_constructors._update_database_constructors(constructors)
    assert mock_db.session.add.call_count == 1
    assert mock_db.session.commit.call_count == 1
