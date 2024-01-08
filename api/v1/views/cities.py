#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


@app_views.route("/states/<state_id>/cities", methods=["GET"])
@app_views.route("/states/<state_id>/cities/", methods=["GET"])
def list_cities_of_state(state_id):
    """This Function Retrieves a list of all City objects"""
    loc_all_states = storage.all("State").values()
    loc_state_obj = [obj.to_dict() for obj in loc_all_states if obj.id == state_id]
    if loc_state_obj == []:
        abort(404)
    loc_list_cities = [
        obj.to_dict()
        for obj in storage.all("City").values()
        if state_id == obj.state_id
    ]
    return jsonify(loc_list_cities)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
@app_views.route("/states/<state_id>/cities/", methods=["POST"])
def create_city(state_id):
    """This Function Creates a City"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    loc_all_states = storage.all("State").values()
    loc_state_obj = [obj.to_dict() for obj in loc_all_states if obj.id == state_id]
    if loc_state_obj == []:
        abort(404)
    loc_cities = []
    loc_new_city = City(name=request.json["name"], state_id=state_id)
    storage.new(loc_new_city)
    storage.save()
    loc_cities.append(loc_new_city.to_dict())
    return jsonify(loc_cities[0]), 201


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """This Function Retrieves a City object"""
    loc_all_cities = storage.all("City").values()
    loc_city_obj = [obj.to_dict() for obj in loc_all_cities if obj.id == city_id]
    if loc_city_obj == []:
        abort(404)
    return jsonify(loc_city_obj[0])


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """This Function Deletes a City object"""
    loc_all_cities = storage.all("City").values()
    loc_city_obj = [obj.to_dict() for obj in loc_all_cities if obj.id == city_id]
    if loc_city_obj == []:
        abort(404)
    loc_city_obj.remove(loc_city_obj[0])
    for obj in loc_all_cities:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>", methods=["PUT"])
def updates_city(city_id):
    """This Function Updates a City object"""
    loc_all_cities = storage.all("City").values()
    loc_city_obj = [obj.to_dict() for obj in loc_all_cities if obj.id == city_id]
    if loc_city_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    loc_city_obj[0]["name"] = request.json["name"]
    for obj in loc_all_cities:
        if obj.id == city_id:
            obj.name = request.json["name"]
    storage.save()
    return jsonify(loc_city_obj[0]), 200
