from app import Circuit, Event, Round, create_app
from app.extensions import db
from app.services import CURRENT_YEAR
from app.services.fetch_rounds import _fetch_rounds_from_jolpica


def run():
    data = _fetch_rounds_from_jolpica(CURRENT_YEAR)
    data = _transform_events_data(data)
    _update_database_events(data)


def _transform_events_data(data):
    transformed = []
    for entry in data:
        circuit = Circuit.query.filter_by(
            external_id=entry["Circuit"]["circuitId"],
        ).one_or_none()
        current_round = Round.query.filter_by(
            year=entry["season"],
            round_number=entry["round"],
        ).one_or_none()

        if "Sprint" in entry:
            transformed.append(
                {
                    "round_id": current_round.id,
                    "circuit_id": circuit.id,
                    "date": entry["Sprint"]["date"],
                    "event_type": "sprint_race",
                }
            )
        transformed.append(
            {
                "round_id": current_round.id,
                "circuit_id": circuit.id,
                "date": entry["Qualifying"]["date"],
                "event_type": "qualifying",
            }
        )
        transformed.append(
            {
                "round_id": current_round.id,
                "circuit_id": circuit.id,
                "date": entry["date"],
                "event_type": "race",
            }
        )

    return transformed


def _update_database_events(data):
    for entry in data:
        existing_entry = Event.query.filter_by(
            round_id=entry["round_id"],
            event_type=entry["event_type"],
        ).one_or_none()
        if existing_entry:
            for key, value in entry.items():
                setattr(existing_entry, key, value)
        else:
            existing_entry = Event(**entry)
            db.session.add(existing_entry)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run()
