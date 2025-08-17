from sqlalchemy import UniqueConstraint

from app.extensions import db


class Event(db.Model):
    __tablename__ = "events"
    __table_args__ = (
        UniqueConstraint(
            "round_id", "event_type", name="idx_events_on_round_id_and_event_type"
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey("rounds.id"), nullable=False)
    circuit_id = db.Column(db.Integer, db.ForeignKey("circuits.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    event_type = db.Column(db.String(255), nullable=False)