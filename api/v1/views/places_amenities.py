#!/usr/bin/python3
"""This Handles all RESTful API actions for `place_amenity` relationship"""
from flask import jsonify, abort

from api.v1.views import app_views
from models.place import Place
from models import storage
from models import storage_t as storage_type
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities")
def amenities_of_a_place(place_id):
    """This Function Retrieve all amenities of a place."""
    locplace = storage.get(Place, place_id)
    if not locplace:
        abort(404)
    result = []

    if storage_type == "db":
        for amenity in locplace.amenities:
            result.append(amenity.to_dict())
    else:
        result = locplace.amenities

    return jsonify(result)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"])
def unlink_amenity_from_a_place(place_id, amenity_id):
    """This Function Unlink amenity from a place."""
    locplace = storage.get(Place, place_id)
    locamenity = storage.get(Amenity, amenity_id)
    if not locplace:
        abort(404)
    if not locamenity:
        abort(404)
    if locamenity not in locplace.amenities:
        abort(404)

    if storage_type == "db":
        locplace.amenities.remove(locamenity)
    else:
        locplace.amenity_ids.remove(locamenity)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_amenity_to_a_place(place_id, amenity_id):
    """This Function Link amenity to a place."""
    locplace = storage.get(Place, place_id)
    locamenity = storage.get(Amenity, amenity_id)
    if not locplace:
        abort(404)
    if not locamenity:
        abort(404)
    if locamenity in locplace.amenities:
        return jsonify(locamenity.to_dict())

    if storage_type == "db":
        locplace.amenities.append(locamenity)
    else:
        locplace.amenity_ids.append(locamenity.id)
    storage.save()

    return jsonify(locamenity.to_dict()), 201
