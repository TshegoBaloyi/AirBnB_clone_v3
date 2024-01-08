#!/usr/bin/python3
"""Handles all RESTful API actions for `place_reviews` relationship"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, request, abort


@app_views.route("/places/<place_id>/reviews")
def reviews_of_a_place(place_id):
    """This Function Get all reviews of a place."""
    locplace = storage.get(Place, place_id)
    if not locplace:
        abort(404)
    result = []

    for review in locplace.reviews:
        result.append(review.to_dict())

    return jsonify(result)


@app_views.route("/reviews/<review_id>")
def review(review_id):
    """This Function Get a review."""
    locreview = storage.get(Review, review_id)
    if not locreview:
        abort(404)

    return jsonify(locreview.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """This Function Remove a review."""
    locreview = storage.get(Review, review_id)
    if not locreview:
        abort(404)

    locreview.delete()
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """This Function Create a review."""
    locplace = storage.get(Place, place_id)
    locpayload = request.get_json()
    if not locplace:
        abort(404)
    if not locpayload:
        abort(400, "Not a JSON")
    if "user_id" not in locpayload:
        abort(400, "Missing user_id")
    if not storage.get(User, locpayload["user_id"]):
        abort(404)
    if "text" not in locpayload:
        abort(400, "Missing text")

    review = Review(place_id=place_id, **locpayload)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """This Function Update a review."""
    locreview = storage.get(Review, review_id)
    locpayload = request.get_json()
    if not locreview:
        abort(404)
    if not locpayload:
        abort(400, "Not a JSON")

    for key, value in locreview.to_dict().items():
        if key not in [
                "id",
                "user_id",
                "place_id",
                "created_at",
                "updated_at",
                "__class__",
                ]:
            setattr(locreview, key, locpayload[key] if key in locpayload else value)
    locreview.save()

    return jsonify(locreview.to_dict())
