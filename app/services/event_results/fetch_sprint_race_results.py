from app import Constructor, Driver, Event, Round, create_app
from app.clients.jolpica_client import fetch_from_jolpica
from app.services import CURRENT_YEAR, MAX_LIMIT
from app.services.event_results import fetch_event_results


def run(year):
    data = _fetch_sprint_race_results_from_jolpica(year)
    data = _transform_sprint_race_results_data(data)
    fetch_event_results.update_database_event_results(data)


def _fetch_sprint_race_results_from_jolpica(year):
    entries = []
    offset = 0
    limit = MAX_LIMIT

    while True:
        data = fetch_from_jolpica(f"{year}/sprint", {"limit": limit, "offset": offset})
        returned = data["MRData"]["RaceTable"]["Races"]
        if not returned:
            break
        entries.extend(returned)
        if len(returned) < limit:
            break
        offset += limit

    return entries


def _transform_sprint_race_results_data(data):
    transformed = []
    for entry in data:
        current_round = Round.query.filter_by(
            year=entry["season"],
            round_number=entry["round"],
        ).one_or_none()
        current_event = Event.query.filter_by(
            event_type="sprint_race",
            round_id=current_round.id,
        ).one_or_none()

        for race_result in entry["SprintResults"]:
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





if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run(CURRENT_YEAR)