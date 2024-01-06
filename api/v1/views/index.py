#!/usr/bin/python3
"""This script contains blueprints for the application"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status")
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def get_stats():
    """Retrieves the number of each object by type"""
    classes = {
            "states": State, "cities": City, "amenities": Amenity,
            "places": Place, "reviews": Review, "users": User
            }
    stats = {k: storage.count(v) for k, v in classes.items()}
    return jsonify(stats)
