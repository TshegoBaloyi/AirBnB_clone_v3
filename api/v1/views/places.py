#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid


@app_views.route("/cities/<city_id>/places", methods=["GET"])
@app_views.route("/cities/<city_id>/places/", methods=["GET"])
def list_places_of_city(city_id):
    """This Function Retrieves a list of all Place objects in city"""
    loc_all_cities = storage.all("City").values()
    loc_city_obj = [obj.to_dict() for obj in loc_all_cities if obj.id == city_id]
    if loc_city_obj == []:
        abort(404)
    loc_list_places = [
        obj.to_dict() for obj in storage.all("Place").values() if city_id == obj.city_id
    ]
    return jsonify(loc_list_places)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """THis Function Retrieves a Place object"""
    loc_all_places = storage.all("Place").values()
    loc_place_obj = [obj.to_dict() for obj in loc_all_places if obj.id == place_id]
    if loc_place_obj == []:
        abort(404)
    return jsonify(loc_place_obj[0])


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """This Function Deletes a Place object"""
    loc_all_places = storage.all("Place").values()
    loc_place_obj = [obj.to_dict() for obj in loc_all_places if obj.id == place_id]
    if loc_place_obj == []:
        abort(404)
    loc_place_obj.remove(loc_place_obj[0])
    for obj in loc_all_places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """This Function Creates a Place"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    loc_all_cities = storage.all("City").values()
    loc_city_obj = [obj.to_dict() for obj in loc_all_cities if obj.id == city_id]
    if loc_city_obj == []:
        abort(404)
    loc_places = []
    loc_new_place = Place(
        name=request.json["name"], user_id=request.json["user_id"], city_id=city_id
    )
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users if obj.id == loc_new_place.user_id]
    if user_obj == []:
        abort(404)
    storage.new(loc_new_place)
    storage.save()
    loc_places.append(loc_new_place.to_dict())
    return jsonify(loc_places[0]), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def updates_place(place_id):
    """This Function Updates a Place object"""
    loc_all_places = storage.all("Place").values()
    loc_place_obj = [obj.to_dict() for obj in loc_all_places if obj.id == place_id]
    if loc_place_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" in request.get_json():
        loc_place_obj[0]["name"] = request.json["name"]
    if "description" in request.get_json():
        loc_place_obj[0]["description"] = request.json["description"]
    if "number_rooms" in request.get_json():
        loc_place_obj[0]["number_rooms"] = request.json["number_rooms"]
    if "number_bathrooms" in request.get_json():
        loc_place_obj[0]["number_bathrooms"] = request.json["number_bathrooms"]
    if "max_guest" in request.get_json():
        loc_place_obj[0]["max_guest"] = request.json["max_guest"]
    if "price_by_night" in request.get_json():
        loc_place_obj[0]["price_by_night"] = request.json["price_by_night"]
    if "latitude" in request.get_json():
        loc_place_obj[0]["latitude"] = request.json["latitude"]
    if "longitude" in request.get_json():
        loc_place_obj[0]["longitude"] = request.json["longitude"]
    for obj in loc_all_places:
        if obj.id == place_id:
            if "name" in request.get_json():
                obj.name = request.json["name"]
            if "description" in request.get_json():
                obj.description = request.json["description"]
            if "number_rooms" in request.get_json():
                obj.number_rooms = request.json["number_rooms"]
            if "number_bathrooms" in request.get_json():
                obj.number_bathrooms = request.json["number_bathrooms"]
            if "max_guest" in request.get_json():
                obj.max_guest = request.json["max_guest"]
            if "price_by_night" in request.get_json():
                obj.price_by_night = request.json["price_by_night"]
            if "latitude" in request.get_json():
                obj.latitude = request.json["latitude"]
            if "longitude" in request.get_json():
                obj.longitude = request.json["longitude"]
    storage.save()
    return jsonify(loc_place_obj[0]), 200
