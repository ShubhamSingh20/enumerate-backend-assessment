from flask import jsonify
from app import app

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify(message="pong")
