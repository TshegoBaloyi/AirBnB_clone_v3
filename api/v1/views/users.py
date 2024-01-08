#!/usr/bin/python3
"""This Handles all RESTful API actions for `User`"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User
from hashlib import md5


@app_views.route("/users")
def users():
    """This Function Get all users."""
    locusers = storage.all(User)
    locresult = []

    for user in locusers.values():
        locresult.append(user.to_dict())

    return jsonify(locresult)


@app_views.route("/users/<user_id>")
def one_user(user_id):
    """This function Get one user."""
    locuser = storage.get(User, user_id)
    if not locuser:
        abort(404)

    return jsonify(locuser.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """This Function Delete user."""
    locuser = storage.get(User, user_id)
    if not locuser:
        abort(404)

    locuser.delete()
    storage.save()

    return jsonify({})


@app_views.route("/users", methods=["POST"])
def create_user():
    """This Function Create user."""
    locpayload = request.get_json()
    if not locpayload:
        abort(400, "Not a JSON")
    if "email" not in locpayload:
        abort(400, "Missing email")
    if "password" not in locpayload:
        abort(400, "Missing password")

    user = User(**locpayload)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """This Function Update user."""
    user = storage.get(User, user_id)
    payload = request.get_json()
    if not user:
        abort(404)
    if not payload:
        abort(400, description="Not a JSON")

    for key, value in user.to_dict().items():
        if key not in ["id", "email", "created_at", "updated_at", "__class__"]:
            if key in payload:
                if key == "password":
                    setattr(user, key, md5(str(payload[key]).encode()).hexdigest())
                else:
                    setattr(user, key, payload[key] if key in payload else value)
    user.save()

    return jsonify(user.to_dict())
