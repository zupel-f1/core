from app import create_app
from app.clients.jolpica_client import fetch_from_jolpica
from app.extensions import db
from app.models.constructor import Constructor
from app.services import MAX_LIMIT


def run():
    constructors = _fetch_constructors_from_jolpica()
    constructors = _transform_constructors_data(constructors)
    _update_database_constructors(constructors)


def _fetch_constructors_from_jolpica():
    all_constructors = []
    offset = 0
    limit = MAX_LIMIT
    while True:
        constructors_data = fetch_from_jolpica(
            "constructors", {"limit": limit, "offset": offset}
        )
        returned_constructors = constructors_data["MRData"]["ConstructorTable"][
            "Constructors"
        ]
        if not returned_constructors:
            break
        all_constructors.extend(returned_constructors)
        if len(returned_constructors) < limit:
            break
        offset += limit
    return all_constructors


def _transform_constructors_data(constructors):
    transformed = []
    for constructor in constructors:
        transformed.append(
            {
                "external_id": constructor["constructorId"],
                "url": constructor["url"],
                "name": constructor["name"],
                "nationality": constructor["nationality"],
            }
        )
    return transformed


def _update_database_constructors(constructors):
    for constructor in constructors:
        existing = Constructor.query.filter_by(
            external_id=constructor["external_id"]
        ).one_or_none()
        if not existing:
            constructor = Constructor(
                external_id=constructor["external_id"],
                name=constructor["name"],
                url=constructor["url"],
                nationality=constructor["nationality"],
            )
            db.session.add(constructor)
            continue
        existing.name = constructor["name"]
        existing.url = constructor["url"]
        existing.nationality = constructor["nationality"]
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run()
