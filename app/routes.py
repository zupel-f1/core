from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask API!"})


@main.route("/ping")
def ping():
    return jsonify({"message": "pong"})
