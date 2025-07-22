from app.extensions import db


class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    given_name = db.Column(db.String(255), nullable=False)
    family_name = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(10), nullable=True, unique=True)
    permanent_number = db.Column(db.Integer, nullable=True, unique=True)
