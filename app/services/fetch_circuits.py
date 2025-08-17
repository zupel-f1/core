from app import create_app
from app.clients.jolpica_client import fetch_from_jolpica
from app.extensions import db
from app.models import Circuit
from app.services import MAX_LIMIT


def run():
    circuits = _fetch_circuits_from_jolpica()
    circuits = _transform_circuits_data(circuits)
    _update_database_circuits(circuits)


def _fetch_circuits_from_jolpica():
    all_circuits = []
    offset = 0
    limit = MAX_LIMIT
    while True:
        circuits_data = fetch_from_jolpica(
            "circuits", {"limit": limit, "offset": offset}
        )
        returned_circuits = circuits_data["MRData"]["CircuitTable"]["Circuits"]
        if not returned_circuits:
            break
        all_circuits.extend(returned_circuits)
        if len(returned_circuits) < limit:
            break
        offset += limit
    return all_circuits


def _transform_circuits_data(circuits):
    transformed = []
    for circuit in circuits:
        transformed.append(
            {
                "external_id": circuit["circuitId"],
                "url": circuit["url"],
                "circuit_name": circuit["circuitName"],
                "city": circuit["Location"]["locality"],
                "country": circuit["Location"]["country"],
            }
        )
    return transformed


def _update_database_circuits(circuits):
    for circuit_data in circuits:
        circuit = (
            db.session.query(Circuit)
            .filter(Circuit.external_id == circuit_data["external_id"])
            .one_or_none()
        )
        if circuit:
            for key, value in circuit_data.items():
                setattr(circuit, key, value)
        else:
            circuit = Circuit(**circuit_data)
            db.session.add(circuit)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run()