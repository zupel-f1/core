import pytest
from unittest.mock import patch

from app.services import fetch_seasons

@pytest.fixture
def sample_season_data():
    return [
        {
            "season": "1950",
            "url": "https://en.wikipedia.org/wiki/1950_Formula_One_season"
        },
        {
            "season": "1951",
            "url": "https://en.wikipedia.org/wiki/1951_Formula_One_season"
        } 
    ]

@patch("app.services.fetch_seasons.fetch_from_jolpica")
def test_fetch_seasons_from_jolpica(mock_fetch):
    mock_fetch.side_effect = [
        {
            "MRData": {
                "SeasonTable": {
                    "Seasons": [
                        {
                            "season": "1950",
                            "url": "https://en.wikipedia.org/wiki/1950_Formula_One_season"
                        },
                        {
                            "season": "1951",
                            "url": "https://en.wikipedia.org/wiki/1951_Formula_One_season"
                        }
                    ]
                }
            }
        }
    ]
    seasons = fetch_seasons._fetch_seasons_from_jolpica()
    assert len(seasons) == 2
    assert seasons[1]["season"] == "1951"

def test_transform_seasons_data(sample_season_data):
    transformed = fetch_seasons._transform_seasons_data(sample_season_data)
    assert transformed == [
        {
        "external_id": "1950",
        "year" : "1950",
        "url" : "https://en.wikipedia.org/wiki/1950_Formula_One_season"
        },
        {
        "external_id": "1951",
        "year" : "1951",
        "url" : "https://en.wikipedia.org/wiki/1951_Formula_One_season"
        }
    ]

@patch("app.services.fetch_seasons.Season")
@patch("app.services.fetch_seasons.db")
def test_update_database_seasons(mock_db, mock_season, sample_season_data):
    mock_db.session.query.return_value.filter.return_value.one_or_none.return_value = None
    seasons = fetch_seasons._transform_seasons_data(sample_season_data)
    fetch_seasons._update_database_seasons(seasons)
    assert mock_db.session.add.call_count == 2
    assert mock_db.session.commit.call_count == 1