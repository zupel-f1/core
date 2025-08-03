from app.clients.jolpica_client import fetch_from_jolpica
from app.services import MAX_LIMIT
from app.models.race import Race
from app import create_app, Circuit, Season
from app.extensions import db
from datetime import datetime


def run():
    app = create_app()
    with app.app_context():
        races = fetch_races_from_jolpica()
        races = transform_races_data(races)
        update_database_races(races)


def fetch_races_from_jolpica():
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


def transform_races_data(races):
    transformed = []
    for race in races:
        season_id = db.session.query(Season).filter(Season.external_id == race["season_id"]).first()
        circuit_id = db.session.query(Circuit).filter(Circuit.external_id == race["circuit_id"]).first()
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


def update_database_races(races):
    for race in races:
        existing = db.session.query(Race).filter(
            Race.season_id == race["season_id"] and Race.circuit_id == race["circuit_id"])
        if existing.count() == 0:
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
        for existing_race in existing.all():
            existing_race.race_name = race["race_name"]
            existing_race.is_sprint = race["is_sprint"]
            existing_race.date = race["date"]
            existing_race.url = race["url"]
            existing_race.round = race["round"]
    db.session.commit()


if __name__ == "__main__":
    run()
