#!/usr/bin/python3
"""places_reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from datetime import datetime
import uuid


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
@app_views.route("/places/<place_id>/reviews/", methods=["GET"])
def list_reviews_of_place(place_id):
    """This Function Retrieves a list of all Review objects of a Place."""
    loc_all_places = storage.all("Place").values()
    loc_place_obj = [obj.to_dict() for obj in loc_all_places if obj.id == place_id]
    if loc_place_obj == []:
        abort(404)
    loc_list_reviews = [
        obj.to_dict()
        for obj in storage.all("Review").values()
        if place_id == obj.place_id
    ]
    return jsonify(loc_list_reviews)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """This Function Creates a Review."""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    loc_user_id = request.json["user_id"]
    if "text" not in request.get_json():
        abort(400, "Missing text")
    loc_all_places = storage.all("Place").values()
    loc_place_obj = [obj.to_dict() for obj in loc_all_places if obj.id == place_id]
    if loc_place_obj == []:
        abort(404)
    loc_all_users = storage.all("User").values()
    loc_user_obj = [obj.to_dict() for obj in loc_all_users if obj.id == loc_user_id]
    if loc_user_obj == []:
        abort(404)
    loc_reviews = []
    loc_new_review = Review(text=request.json["text"], place_id=place_id, user_id=loc_user_id)
    storage.new(loc_new_review)
    storage.save()
    loc_reviews.append(loc_new_review.to_dict())
    return jsonify(loc_reviews[0]), 201


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """This Function Retrieves a Review object."""
    loc_all_reviews = storage.all("Review").values()
    loc_review_obj = [obj.to_dict() for obj in loc_all_reviews if obj.id == review_id]
    if loc_review_obj == []:
        abort(404)
    return jsonify(loc_review_obj[0])


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """This Function Deletes a Review object"""
    loc_all_reviews = storage.all("Review").values()
    loc_review_obj = [obj.to_dict() for obj in loc_all_reviews if obj.id == review_id]
    if loc_review_obj == []:
        abort(404)
    loc_review_obj.remove(loc_review_obj[0])
    for obj in loc_all_reviews:
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def updates_review(review_id):
    """This Function Updates a Review object"""
    loc_all_reviews = storage.all("Review").values()
    loc_review_obj = [obj.to_dict() for obj in loc_all_reviews if obj.id == review_id]
    if loc_review_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "text" in request.get_json():
        loc_review_obj[0]["text"] = request.json["text"]
        for obj in loc_all_reviews:
            if obj.id == review_id:
                obj.text = request.json["text"]
        storage.save()
    return jsonify(loc_review_obj[0]), 200

