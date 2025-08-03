from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@main.route('/ping')
def ping():
    return jsonify({"message": "pong"})

@main.route('/drivers')
def get_drivers():
    from app.services.fetch_drivers import run as fetch_drivers
    try:
        fetch_drivers()
        return jsonify({"message": "Drivers fetched successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
