from app.extensions import db


class ConstructorStanding(db.Model):
    __tablename__ = 'constructor_standings'
    __table_args__ = (
        db.UniqueConstraint('constructor_id', 'season_id', 'round', name='idx_constructor_standings_on_constructor_id_season_id_and_round'),
    )
    id = db.Column(db.Integer, primary_key=True)
    constructor_id = db.Column(db.Integer, db.ForeignKey('constructors.id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    round = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Float, nullable=False)
    position = db.Column(db.Integer, nullable=False)