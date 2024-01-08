#!/usr/bin/python3
"""This Handles all RESTful API actions for `Amenity`"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

from flask import jsonify, abort, request


@app_views.route("/amenities")
def amenities():
    """This Function Retrieve list of all `Amenity` objects"""
    locamenities = storage.all(Amenity)
    locresult = []

    for amenity in locamenities.values():
        locresult.append(amenity.to_dict())

    return jsonify(locresult)


@app_views.route("/amenities/<amenity_id>")
def amenity(amenity_id):
    """This Function Retrieve one `Amenity`"""
    locamenity = storage.get(Amenity, amenity_id)
    if not locamenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """This Function Delete an amenity."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """This Function Create an amenity."""
    locpayload = request.get_json()
    if not locpayload:
        abort(400, "Not a JSON")
    if "name" not in locpayload:
        abort(400, "Missing name")

    amenity = Amenity(**locpayload)
    amenity.save()

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    locamenity = storage.get(Amenity, amenity_id)
    locpayload = request.get_json()
    if not locamenity:
        abort(404)
    if not locpayload:
        abort(400, "Not a JSON")

    key = "name"
    setattr(locamenity, key, locpayload[key])
    locamenity.save()

    return jsonify(locamenity.to_dict())
