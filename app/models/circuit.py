from app.extensions import db


class Circuit(db.Model):
    __tablename__ = 'circuits'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    circuit_name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country_emoji = db.Column(db.String(100), nullable=False)
