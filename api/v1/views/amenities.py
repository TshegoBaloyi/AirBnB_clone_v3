#!/usr/bin/python3
"""amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route("/amenities/", methods=["GET"])
def list_amenities():
    """This function Retrieves a list of all Amenity objects"""
    loc_list_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(loc_list_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """'this Function Retrieves an Amenity object"""
    loc_all_amenities = storage.all("Amenity").values()
    loc_amenity_obj = [
        obj.to_dict() for obj in loc_all_amenities if obj.id == amenity_id
    ]
    if loc_amenity_obj == []:
        abort(404)
    return jsonify(loc_amenity_obj[0])


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """This Function Deletes an Amenity object"""
    loc_all_amenities = storage.all("Amenity").values()
    loc_amenity_obj = [
        obj.to_dict() for obj in loc_all_amenities if obj.id == amenity_id
    ]
    if loc_amenity_obj == []:
        abort(404)
    loc_amenity_obj.remove(loc_amenity_obj[0])
    for obj in loc_all_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/", methods=["POST"])
def create_amenity():
    """This Function Creates an Amenity"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    loc_amenities = []
    loc_new_amenity = Amenity(name=request.json["name"])
    storage.new(loc_new_amenity)
    storage.save()
    loc_amenities.append(loc_new_amenity.to_dict())
    return jsonify(loc_amenities[0]), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def updates_amenity(amenity_id):
    """This Function Updates an Amenity object"""
    loc_all_amenities = storage.all("Amenity").values()
    loc_amenity_obj = [
        obj.to_dict() for obj in loc_all_amenities if obj.id == amenity_id
    ]
    if loc_amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    loc_amenity_obj[0]["name"] = request.json["name"]
    for obj in loc_all_amenities:
        if obj.id == amenity_id:
            obj.name = request.json["name"]
    storage.save()
    return jsonify(loc_amenity_obj[0]), 200
