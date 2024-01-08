#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    "users": "User",
    "places": "Place",
    "states": "State",
    "cities": "City",
    "amenities": "Amenity",
    "reviews": "Review",
}


@app_views.route("/status", methods=["GET"])
def status():
    """This Function routes to status page"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def count():
    """This Function retrieves the number of each objects by type"""
    loc_count_dict = {}
    for cls in classes:
        loc_count_dict[cls] = storage.count(classes[cls])
    return jsonify(loc_count_dict)
