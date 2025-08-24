from app import EventResult, create_app, db
from app.services import CURRENT_YEAR
from app.services.event_results import (
    fetch_sprint_race_results,
    fetch_qualifying_results,
    fetch_race_results,
)


def run(year):
    fetch_race_results.run(year)
    fetch_qualifying_results.run(year)
    fetch_sprint_race_results.run(year)


def update_database_event_results(data):
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