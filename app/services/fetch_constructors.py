from app.clients.jolpica_client import fetch_from_jolpica
from app.services import MAX_LIMIT
from app.models.constructor import Constructor
from app import create_app
from app.extensions import db


def run():
    app = create_app()
    with app.app_context():
        constructors = fetch_constructors_from_jolpica()
        constructors = transform_constructors_data(constructors)
        update_database_constructors(constructors)


def fetch_constructors_from_jolpica():
    all_constructors = []
    offset = 0
    limit = MAX_LIMIT
    while True:
        constructors_data = fetch_from_jolpica("constructors", {"limit": limit, "offset": offset})
        returned_constructors = constructors_data["MRData"]["ConstructorTable"]["Constructors"]
        if not returned_constructors:
            break
        all_constructors.extend(returned_constructors)
        if len(returned_constructors) < limit:
            break
        offset += limit
    return all_constructors


def transform_constructors_data(constructors):
    transformed = []
    for constructor in constructors:
        transformed.append({
            "external_id": constructor["constructorId"],
            "url": constructor["url"],
            "name": constructor["name"],
            "nationality": constructor["nationality"],
        })
    return transformed


def update_database_constructors(constructors):
    for constructor in constructors:
        existing = db.session.query(Constructor).filter(Constructor.external_id == constructor["external_id"])
        if existing.count() == 0:
            constructor = Constructor(
                external_id=constructor["external_id"],
                name=constructor["name"],
                url=constructor["url"],
                nationality=constructor["nationality"],
            )
            db.session.add(constructor)
            continue
        for existing_constructor in existing.all():
            existing_constructor.name = constructor["name"]
            existing_constructor.url = constructor["url"]
            existing_constructor.nationality = constructor["nationality"]
    db.session.commit()


if __name__ == "__main__":
    run()
