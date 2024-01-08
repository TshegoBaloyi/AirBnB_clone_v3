#!/usr/bin/python3
"""places_amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
@app_views.route("/places/<place_id>/amenities/", methods=["GET"])
def list_amenities_of_place(place_id):
    """This Function Retrieves a list of all Amenity objects of a Place"""
    loc_all_places = storage.all("Place").values()
    loc_place_obj = [obj.to_dict() for obj in loc_all_places if obj.id == place_id]
    if loc_place_obj == []:
        abort(404)
    loc_list_amenities = []
    for obj in loc_all_places:
        if obj.id == place_id:
            for amenity in obj.amenities:
                loc_list_amenities.append(amenity.to_dict())
    return jsonify(loc_list_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def create_place_amenity(place_id, amenity_id):
    """This function Creates a Amenity"""
    loc_all_places = storage.all("Place").values()
    loc_place_obj = [obj.to_dict() for obj in loc_all_places if obj.id == place_id]
    if loc_place_obj == []:
        abort(404)

    loc_all_amenities = storage.all("Amenity").values()
    loc_amenity_obj = [
        obj.to_dict() for obj in loc_all_amenities if obj.id == amenity_id
    ]
    if loc_amenity_obj == []:
        abort(404)

    loc_amenities = []
    for place in loc_all_places:
        if place.id == place_id:
            for amenity in loc_all_amenities:
                if amenity.id == amenity_id:
                    place.amenities.append(amenity)
                    storage.save()
                    loc_amenities.append(amenity.to_dict())
                    return jsonify(loc_amenities[0]), 200
    return jsonify(loc_amenities[0]), 201


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """This Function Deletes a Amenity object"""
    loc_all_places = storage.all("Place").values()
    loc_place_obj = [obj.to_dict() for obj in loc_all_places if obj.id == place_id]
    if loc_place_obj == []:
        abort(404)

    loc_all_amenities = storage.all("Amenity").values()
    loc_amenity_obj = [
        obj.to_dict() for obj in loc_all_amenities if obj.id == amenity_id
    ]
    if loc_amenity_obj == []:
        abort(404)
    loc_amenity_obj.remove(loc_amenity_obj[0])

    for obj in loc_all_places:
        if obj.id == place_id:
            if obj.amenities == []:
                abort(404)
            for amenity in obj.amenities:
                if amenity.id == amenity_id:
                    storage.delete(amenity)
                    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_place_amenity(amenity_id):
    """This Function Retrieves a Amenity object"""
    loc_all_amenities = storage.all("Amenity").values()
    loc_amenity_obj = [
        obj.to_dict() for obj in loc_all_amenities if obj.id == amenity_id
    ]
    if loc_amenity_obj == []:
        abort(404)
    return jsonify(loc_amenity_obj[0])
