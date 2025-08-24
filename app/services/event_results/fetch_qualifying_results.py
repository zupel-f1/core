from app import Constructor, Driver, Event, Round, create_app
from app.clients.jolpica_client import fetch_from_jolpica
from app.services import CURRENT_YEAR, MAX_LIMIT
from app.services.event_results import fetch_event_results


def run(year):
    data = _fetch_qualifying_results_from_jolpica(year)
    data = _transform_qualifying_results_data(data)
    fetch_event_results.update_database_event_results(data)


def _fetch_qualifying_results_from_jolpica(year):
    entries = []
    offset = 0
    limit = MAX_LIMIT

    while True:
        data = fetch_from_jolpica(
            f"{year}/qualifying", {"limit": limit, "offset": offset}
        )
        returned = data["MRData"]["RaceTable"]["Races"]
        if not returned:
            break
        entries.extend(returned)
        if len(returned) < limit:
            break
        offset += limit

    return entries


def _transform_qualifying_results_data(data):
    transformed = []
    for entry in data:
        current_round = Round.query.filter_by(
            year=entry["season"],
            round_number=entry["round"],
        ).one_or_none()
        current_event = Event.query.filter_by(
            event_type="qualifying",
            round_id=current_round.id,
        ).one_or_none()

        for result in entry["QualifyingResults"]:
            driver = Driver.query.filter_by(
                external_id=result["Driver"]["driverId"],
            ).one_or_none()
            constructor = Constructor.query.filter_by(
                external_id=result.get("Constructor", {}).get("constructorId"),
            ).one_or_none()

            t_str = result.get("Q3") or result.get("Q2") or result.get("Q1")
            time = to_millis(t_str) if t_str else None

            transformed.append(
                {
                    "event_id": current_event.id,
                    "driver_id": driver.id,
                    "constructor_id": constructor.id if constructor else None,
                    "position": result.get("position"),
                    "time": time,
                }
            )

    return transformed

def to_millis(s: str) -> int:
    m, rest = s.split(':')
    sec, ms = rest.split('.')
    return int(m)*60_000 + int(sec)*1_000 + int(ms)

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run(CURRENT_YEAR)