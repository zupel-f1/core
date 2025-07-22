from app.extensions import db


class Constructor(db.Model):
    __tablename__ = 'constructors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)