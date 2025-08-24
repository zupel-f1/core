from app import Constructor, ConstructorStanding, Round, create_app
from app.clients.jolpica_client import fetch_from_jolpica
from app.extensions import db
from app.services import CURRENT_YEAR, MAX_LIMIT


def run():
    data = _fetch_constructor_standings_from_jolpica(CURRENT_YEAR)
    data = _transform_constructor_standings_data(data)
    _update_database_constructor_standings(data)


def _fetch_constructor_standings_from_jolpica(year):
    entries = []
    offset = 0
    limit = MAX_LIMIT

    newest_data = fetch_from_jolpica(
        f"{year}/constructorstandings", {"limit": limit, "offset": offset}
    )
    newest_round = newest_data["MRData"]["StandingsTable"]["round"]

    for i in range(1, int(newest_round) + 1):
        while True:
            data = fetch_from_jolpica(
                f"{year}/{i}/constructorstandings", {"limit": limit, "offset": offset}
            )
            returned = data["MRData"]["StandingsTable"]["StandingsLists"]
            if not returned:
                break
            entries.extend(returned)
            if len(returned) < limit:
                break
            offset += limit
    return entries


def _transform_constructor_standings_data(data):
    transformed = []
    for entry in data:
        current_round = Round.query.filter_by(
            year=entry["season"],
            round_number=entry["round"],
        ).one_or_none()

        for constructor_standing in entry["ConstructorStandings"]:
            current_constructor = Constructor.query.filter_by(
                external_id=constructor_standing["Constructor"]["constructorId"],
            ).one_or_none()

            transformed.append(
                {
                    "constructor_id": current_constructor.id,
                    "round_id": current_round.id,
                    "points": constructor_standing["points"],
                    "position": constructor_standing.get("position"),
                }
            )

    return transformed


def _update_database_constructor_standings(data):
    for entry in data:
        existing_entry = ConstructorStanding.query.filter_by(
            constructor_id=entry["constructor_id"],
            round_id=entry["round_id"],
        ).one_or_none()
        if existing_entry:
            for key, value in entry.items():
                setattr(existing_entry, key, value)
        else:
            existing_entry = ConstructorStanding(**entry)
            db.session.add(existing_entry)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run()