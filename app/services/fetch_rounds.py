from app import Round, create_app
from app.clients.jolpica_client import fetch_from_jolpica
from app.extensions import db
from app.services import CURRENT_YEAR, MAX_LIMIT


def run():
    rounds = _fetch_rounds_from_jolpica(CURRENT_YEAR)
    rounds = _transform_rounds_data(rounds)
    _update_database_rounds(rounds)


def _fetch_rounds_from_jolpica(year):
    all_rounds = []
    offset = 0
    limit = MAX_LIMIT
    while True:
        rounds_data = fetch_from_jolpica(
            f"{year}/races", {"limit": limit, "offset": offset}
        )
        returned_rounds = rounds_data["MRData"]["RaceTable"]["Races"]
        if not returned_rounds:
            break
        all_rounds.extend(returned_rounds)
        if len(returned_rounds) < limit:
            break
        offset += limit
    return all_rounds


def _transform_rounds_data(rounds):
    transformed = []
    for round_entry in rounds:
        transformed.append(
            {
                "year": round_entry["season"],
                "round_number": round_entry["round"],
                "race_name": round_entry["raceName"],
            }
        )
    return transformed


def _update_database_rounds(rounds):
    for round_data in rounds:
        existing_round = Round.query.filter_by(
            year=round_data["year"],
            round_number=round_data["round_number"],
        ).one_or_none()
        if existing_round:
            for key, value in round_data.items():
                setattr(existing_round, key, value)
        else:
            existing_round = Round(**round_data)
            db.session.add(existing_round)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run()
