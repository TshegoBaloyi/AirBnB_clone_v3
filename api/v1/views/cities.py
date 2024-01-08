#!/usr/bin/python3
"""This Handles all RESTful API actions for `City`"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities")
def cities_in_a_state(state_id):
    """This function Retrieve the list of all `City` objects of a state"""
    locstate = storage.get(State, state_id)
    if not locstate:
        abort(404)

    locresult = []
    for city in locstate.cities:
        locresult.append(city.to_dict())

    return jsonify(locresult)


@app_views.route("/cities/<city_id>")
def city(city_id):
    """This Function Retrieve a `City`"""
    loccity = storage.get(City, city_id)
    if not loccity:
        abort(404)

    return jsonify(loccity.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """This Function Remove a city."""
    loccity = storage.get(City, city_id)
    if not loccity:
        abort(404)

    loccity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """This Function Create a city."""
    locstate = storage.get(State, state_id)
    if not locstate:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")

    loccity = City(state_id=state_id, **request.get_json())
    loccity.save()

    return jsonify(loccity.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """This Function updates a city."""
    loccity = storage.get(City, city_id)
    if not loccity:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    key = "name"
    setattr(loccity, key, request.get_json().get(key))
    loccity.save()

    return jsonify(loccity.to_dict())
