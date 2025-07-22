from app.extensions import db


class RaceDriverResult(db.Model):
    __tablename__ = 'race_driver_results'

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    constructor_id = db.Column(db.Integer, db.ForeignKey('constructors.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    laps = db.Column(db.Integer, nullable=False)
