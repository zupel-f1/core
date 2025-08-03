from app.clients.jolpica_client import fetch_from_jolpica
from app.extensions import db
from app.models.driver import Driver

def run():
    drivers = _fetch_drivers_from_jolpica()
    drivers = _transform_drivers_data(drivers)
    _update_database_drivers(drivers)

def _fetch_drivers_from_jolpica():
    MAX_LIMIT = 100
    all_drivers = []
    offset = 0
    limit = MAX_LIMIT
    while True:
        drivers_data = fetch_from_jolpica("drivers", {"limit": limit, "offset": offset})
        returned_drivers = drivers_data["MRData"]["DriverTable"]["Drivers"]
        if not returned_drivers:
            break
        all_drivers.extend(returned_drivers)
        if len(returned_drivers) < limit:
            break
        offset += limit
    return all_drivers

def _transform_drivers_data(drivers):
    transformed = []
    for driver in drivers:
        transformed.append({
            "external_id": driver["driverId"],
            "url": driver["url"],
            "given_name": driver["givenName"],
            "family_name": driver["familyName"],
            "nationality": driver["nationality"],
            "date_of_birth": driver["dateOfBirth"],
            "code": driver["code"],
            "permanent_number": driver["permanentNumber"]
        })
    return transformed


def _update_database_drivers(drivers):
     for driver_data in drivers:
        driver = Driver.query.filter_by(external_id=driver_data["external_id"]).first()
        if driver:
            for key, value in driver_data.items():
                setattr(driver, key, value)
        else:
            driver = Driver(**driver_data)
            db.session.add(driver)
            
        db.session.commit()

if __name__ == "__main__":
    run()