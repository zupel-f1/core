from sqlalchemy import UniqueConstraint

from app.extensions import db


class EventResult(db.Model):
    __tablename__ = "event_results"
    __table_args__ = (
        UniqueConstraint(
            "event_id", "driver_id", name="idx_event_results_on_event_id_and_driver_id"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    constructor_id = db.Column(
        db.Integer, db.ForeignKey("constructors.id"), nullable=True
    )
    position = db.Column(db.Integer, nullable=True)
    time = db.Column(db.Integer, nullable=True)
    points = db.Column(db.Float, nullable=True)
    laps = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(100), nullable=False)
    start_position = db.Column(db.Integer, nullable=True)