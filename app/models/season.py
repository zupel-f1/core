from app.extensions import db


class Season(db.Model):
    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(255), nullable=False)
