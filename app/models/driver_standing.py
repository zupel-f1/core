from sqlalchemy import UniqueConstraint

from app.extensions import db


class DriverStanding(db.Model):
    __tablename__ = "driver_standings"
    __table_args__ = (
        UniqueConstraint(
            "driver_id", "round_id", name="idx_driver_standings_on_driver_id_and_round_id"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey("rounds.id"), nullable=False)
    points = db.Column(db.Float, nullable=False)
    position = db.Column(db.Integer, nullable=True)