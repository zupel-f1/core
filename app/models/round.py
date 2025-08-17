from sqlalchemy import UniqueConstraint

from app.extensions import db


class Round(db.Model):
    __tablename__ = "rounds"
    __table_args__ = (
        UniqueConstraint(
            "year", "round_number", name="idx_rounds_on_year_and_round_number"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    round_number = db.Column(db.Integer, nullable=False)
    race_name = db.Column(db.String(255), nullable=False)
