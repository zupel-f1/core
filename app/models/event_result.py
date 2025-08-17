from app.extensions import db


class EventResult(db.Model):
    __tablename__ = 'event_results'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    constructor_id = db.Column(db.Integer, db.ForeignKey('constructors.id'), nullable=True)
    position = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    laps = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Boolean, nullable=True)
    start_position = db.Column(db.Integer, nullable=True)