from sqlalchemy import UniqueConstraint

from app.extensions import db


class ConstructorStanding(db.Model):
    __tablename__ = "constructor_standings"
    __table_args__ = (
        UniqueConstraint(
            "constructor_id", "round_id", name="idx_constructor_standings_on_constructor_id_and_round_id"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    constructor_id = db.Column(db.Integer, db.ForeignKey("constructors.id"), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey("rounds.id"), nullable=False)
    points = db.Column(db.Float, nullable=False)
    position = db.Column(db.Integer, nullable=True)