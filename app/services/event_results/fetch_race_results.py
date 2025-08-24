from app import (
    Constructor,
    Driver,
    Event,
    EventResult,
    Round,
    create_app,
)
from app.clients.jolpica_client import fetch_from_jolpica
from app.extensions import db
from app.services import CURRENT_YEAR, MAX_LIMIT


def run(year):
    data = _fetch_race_results_from_jolpica(year)
    data = _transform_race_results_data(data)
    _update_database_race_results(data)


def _fetch_race_results_from_jolpica(year):
    entries = []
    offset = 0
    limit = MAX_LIMIT

    while True:
        data = fetch_from_jolpica(f"{year}/results", {"limit": limit, "offset": offset})
        returned = data["MRData"]["RaceTable"]["Races"]
        if not returned:
            break
        entries.extend(returned)
        if len(returned) < limit:
            break
        offset += limit

    return entries


def _transform_race_results_data(data):
    transformed = []
    for entry in data:
        current_round = Round.query.filter_by(
            year=entry["season"],
            round_number=entry["round"],
        ).one_or_none()
        current_event = Event.query.filter_by(
            event_type="race",
            round_id=current_round.id,
        ).one_or_none()

        for race_result in entry["Results"]:
            driver = Driver.query.filter_by(
                external_id=race_result["Driver"]["driverId"],
            ).one_or_none()
            constructor = Constructor.query.filter_by(
                external_id=race_result.get("Constructor", {}).get("constructorId"),
            ).one_or_none()

            transformed.append(
                {
                    "event_id": current_event.id,
                    "driver_id": driver.id,
                    "constructor_id": constructor.id if constructor else None,
                    "position": race_result["position"],
                    "time": race_result.get("Time", {}).get("millis"),
                    "points": race_result["points"],
                    "laps": race_result.get("laps"),
                    "status": race_result.get("status"),
                    "start_position": race_result.get("grid"),
                }
            )

    return transformed


def _update_database_race_results(data):
    for entry in data:
        existing_entry = EventResult.query.filter_by(
            event_id=entry["event_id"],
            driver_id=entry["driver_id"],
        ).one_or_none()
        if existing_entry:
            for key, value in entry.items():
                setattr(existing_entry, key, value)
        else:
            existing_entry = EventResult(**entry)
            db.session.add(existing_entry)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run(CURRENT_YEAR)