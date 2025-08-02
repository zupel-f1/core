from app.extensions import db
from sqlalchemy import UniqueConstraint

class Race(db.Model):
    __tablename__ = 'races'
    __table_args__ = (
        UniqueConstraint('season_id', 'round', name='idx_races_on_season_id_and_round'),
    )
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    circuit_id = db.Column(db.Integer, db.ForeignKey('circuits.id'), nullable=False)
    race_name = db.Column(db.String(255), nullable=False)
    is_sprint = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    round = db.Column(db.Integer, nullable=False)
