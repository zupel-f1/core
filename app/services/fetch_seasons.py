from app.clients.jolpica_client import fetch_from_jolpica
from app.services import MAX_LIMIT
from app.models import Season
from app import create_app
from app.extensions import db

def run():
    seasons = _fetch_seasons_from_jolpica()
    seasons = _transform_seasons_data(seasons)
    _update_database_seasons(seasons)

def _fetch_seasons_from_jolpica():
    all_seasons = []
    offset = 0
    limit = MAX_LIMIT
    while True:
        seasons_data = fetch_from_jolpica("seasons", {"limit" : limit, "offset" : offset})
        returned_seasons = seasons_data["MRData"]["SeasonTable"]["Seasons"]
        if not returned_seasons:
            break
        all_seasons.extend(returned_seasons)
        if len(returned_seasons) < limit:
            break
        offset += limit
    return all_seasons

def _transform_seasons_data(seasons):
    transformed = []
    for season in seasons:
        transformed.append({
            "external_id": season["season"],
            "year" : season["season"],
            "url" : season["url"]
        })
    return transformed

def _update_database_seasons(seasons):
    for season_data in seasons:
        season = db.session.query(Season).filter(Season.external_id == season_data["external_id"]).one_or_none()
        if season:
            for key, value in season_data.items():
                setattr(season, key, value)
        else:
            season = Season(**season_data) 
            db.session.add(season)
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run()