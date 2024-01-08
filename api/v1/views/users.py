#!/usr/bin/python3
"""users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route("/users/", methods=["GET"])
@app_views.route("/users", methods=["GET"])
def list_users():
    """This Function Retrieves a list of all User objects"""
    loc_list_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(loc_list_users)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """This Function Retrieves a User object"""
    loc_all_users = storage.all("User").values()
    loc_user_obj = [obj.to_dict() for obj in loc_all_users if obj.id == user_id]
    if loc_user_obj == []:
        abort(404)
    return jsonify(loc_user_obj[0])


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """This Function Deletes a User object"""
    loc_all_users = storage.all("User").values()
    loc_user_obj = [obj.to_dict() for obj in loc_all_users if obj.id == user_id]
    if loc_user_obj == []:
        abort(404)
    loc_user_obj.remove(loc_user_obj[0])
    for obj in loc_all_users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route("/users/", methods=["POST"])
def create_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing name")
    if "password" not in request.get_json():
        abort(400, "Missing name")
    loc_users = []
    loc_new_user = User(email=request.json["email"], password=request.json["password"])
    storage.new(loc_new_user)
    storage.save()
    loc_users.append(loc_new_user.to_dict())
    return jsonify(loc_users[0]), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def updates_user(user_id):
    """This Function Updates a User object"""
    loc_all_users = storage.all("User").values()
    loc_user_obj = [obj.to_dict() for obj in loc_all_users if obj.id == user_id]
    if loc_user_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    try:
        loc_user_obj[0]["first_name"] = request.json["first_name"]
    except:
        pass
    try:
        loc_user_obj[0]["last_name"] = request.json["last_name"]
    except:
        pass
    for obj in loc_all_users:
        if obj.id == user_id:
            try:
                if request.json["first_name"] is not None:
                    obj.first_name = request.json["first_name"]
            except:
                pass
            try:
                if request.json["last_name"] is not None:
                    obj.last_name = request.json["last_name"]
            except:
                pass
    storage.save()
    return jsonify(loc_user_obj[0]), 200
