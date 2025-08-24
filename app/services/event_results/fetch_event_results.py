from app import create_app
from app.services import CURRENT_YEAR
from app.services.event_results import (
    fetch_race_results,
)


def run(year):
    fetch_race_results.run(year)
    


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run(CURRENT_YEAR)