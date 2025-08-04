from app.clients.jolpica_client import fetch_from_jolpica
from app.services import MAX_LIMIT
from app.models.race import Race
from app import create_app, Circuit, Season
from app.extensions import db
from datetime import datetime


def run():
    races = _fetch_races_from_jolpica()
    races = _transform_races_data(races)
    _update_database_races(races)


def _fetch_races_from_jolpica():
    all_races = []
    offset = 0
    limit = MAX_LIMIT
    while True:
        races_data = fetch_from_jolpica("races", {"limit": limit, "offset": offset})
        returned_races = races_data["MRData"]["RaceTable"]["Races"]
        if not returned_races:
            break
        all_races.extend(returned_races)
        if len(returned_races) < limit:
            break
        offset += limit
    return all_races


def _transform_races_data(races):
    transformed = []
    for race in races:
        season_id = Season.query.filter_by(external_id = race["season"]).one_or_none()
        circuit_id = Circuit.query.filter_by(external_id = race["Circuit"]["circuitId"]).one_or_none()
        if season_id is None or circuit_id is None:
            continue
        transformed.append({
            "season_id": season_id,
            "circuit_id": circuit_id,
            "race_name": race["raceName"],
            "is_sprint": race.get("Sprint") is not None,
            "date": datetime.strptime(race["date"], "%Y-%m-%d").date(),
            "url": race["url"],
            "round": race["round"]})
    return transformed


def _update_database_races(races):
    for race in races:
        existing = Race.query.filter_by(season_id = race["season_id"]).filter_by(round = race["round"]).one_or_none()
        if not existing:
            race = Race(
                season_id=race["season_id"],
                circuit_id=race["circuit_id"],
                race_name=race["race_name"],
                is_sprint=race["is_sprint"],
                date=race["date"],
                url=race["url"],
                round=race["round"],
            )
            db.session.add(race)
            continue
        existing.circuit_id = race["circuit_id"]
        existing.race_name = race["race_name"]
        existing.is_sprint = race["is_sprint"]
        existing.date = race["date"]
        existing.url = race["url"]
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run()
