from app.extensions import db


class DriverStanding(db.Model):
    __tablename__ = 'driver_standings'
    __table_args__ = (
        db.UniqueConstraint('driver_id', 'season_id', 'round', name='idx_driver_standings_on_driver_id_season_id_and_round'),
    )
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    round = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)