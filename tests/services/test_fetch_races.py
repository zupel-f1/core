from datetime import date

import pytest
from unittest.mock import patch

from app import Race
from app.services import fetch_races


@pytest.fixture
def sample_race_data():
    return [
        {
            "season": "2025",
            "round": "1",
            "url": "https://en.wikipedia.org/wiki/2025_Australian_Grand_Prix",
            "raceName": "Australian Grand Prix",
            "Circuit": {
                "circuitId": "albert_park",
                "url": "https://en.wikipedia.org/wiki/Albert_Park_Circuit",
                "circuitName": "Albert Park Grand Prix Circuit",
                "Location": {
                    "lat": "-37.8497",
                    "long": "144.968",
                    "locality": "Melbourne",
                    "country": "Australia"
                }
            },
            "date": "2025-03-16",
            "time": "04:00:00Z",
            "FirstPractice": {
                "date": "2025-03-14",
                "time": "01:30:00Z"
            },
            "SecondPractice": {
                "date": "2025-03-14",
                "time": "05:00:00Z"
            },
            "ThirdPractice": {
                "date": "2025-03-15",
                "time": "01:30:00Z"
            },
            "Qualifying": {
                "date": "2025-03-15",
                "time": "05:00:00Z"
            }
        },
        {
            "season": "2025",
            "round": "2",
            "url": "https://en.wikipedia.org/wiki/2025_Chinese_Grand_Prix",
            "raceName": "Chinese Grand Prix",
            "Circuit": {
                "circuitId": "shanghai",
                "url": "https://en.wikipedia.org/wiki/Shanghai_International_Circuit",
                "circuitName": "Shanghai International Circuit",
                "Location": {
                    "lat": "31.3389",
                    "long": "121.22",
                    "locality": "Shanghai",
                    "country": "China"
                }
            },
            "date": "2025-03-23",
            "time": "07:00:00Z",
            "FirstPractice": {
                "date": "2025-03-21",
                "time": "03:30:00Z"
            },
            "Qualifying": {
                "date": "2025-03-22",
                "time": "07:00:00Z"
            },
            "Sprint": {
                "date": "2025-03-22",
                "time": "03:00:00Z"
            },
            "SprintQualifying": {
                "date": "2025-03-21",
                "time": "07:30:00Z"
            }
        }
    ]


@patch("app.services.fetch_races.fetch_from_jolpica")
def test_fetch_races_from_jolpica(mock_fetch, sample_race_data):
    mock_fetch.side_effect = [
        {
            "MRData": {
                "RaceTable": {
                    "season": "2025",
                    "Races": sample_race_data
                }
            }
        },
        {
            "MRData": {
                "RaceTable": {
                    "Races": []
                }
            }
        }
    ]
    races = fetch_races._fetch_races_from_jolpica()
    assert len(races) == 2
    assert races[0]["season"] == "2025"
    assert races[0]["Circuit"]["circuitId"] == "albert_park"


@patch("app.services.fetch_races.Circuit")
@patch("app.services.fetch_races.Season")
def test_transform_constructors_data(mock_season, mock_circuit, sample_race_data):

    mock_season.query.filter_by.return_value.one_or_none.side_effect = [0, 0]
    mock_circuit.query.filter_by.return_value.one_or_none.side_effect = [0, 1]

    transformed = fetch_races._transform_races_data(sample_race_data)
    assert transformed == [{
        "season_id": 0,
        "circuit_id": 0,
        "race_name": "Australian Grand Prix",
        "is_sprint": False,
        "date": date(2025, 3, 16),
        "url": "https://en.wikipedia.org/wiki/2025_Australian_Grand_Prix",
        "round": "1"
        },
        {"season_id": 0,
         "circuit_id": 1,
         "race_name": "Chinese Grand Prix",
         "is_sprint": True,
         "date": date(2025, 3, 23),
         "url": "https://en.wikipedia.org/wiki/2025_Chinese_Grand_Prix",
         "round": "2"
         }
    ]


@patch("app.services.fetch_races.Circuit")
@patch("app.services.fetch_races.Season")
@patch("app.services.fetch_races.Race")
@patch("app.services.fetch_races.db")
def test_update_database_drivers(mock_db, mock_race, mock_season, mock_circuit, sample_race_data):
    mock_season.query.filter_by.return_value.one_or_none.side_effect = [0, 0]
    mock_circuit.query.filter_by.return_value.one_or_none.side_effect = [0, 1]
    mock_race.query.filter_by.return_value.filter_by.return_value.one_or_none.side_effect = [None, Race(
                season_id=0,
                circuit_id=101,
                race_name=":)",
                is_sprint=False,
                date=date(2005, 10, 3),
                url="https://www.google.com",
                round=2,
            )]

    races = fetch_races._transform_races_data(sample_race_data)
    fetch_races._update_database_races(races)
    assert mock_db.session.add.call_count == 1
    assert mock_db.session.commit.call_count == 1
