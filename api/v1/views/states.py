#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route("/states/", methods=["GET"])
def list_states():
    """This Function Retrieves a list of all State objects"""
    loc_list_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(loc_list_states)


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """This function Retrieves a State object"""
    loc_all_states = storage.all("State").values()
    loc_state_obj = [obj.to_dict() for obj in loc_all_states if obj.id == state_id]
    if loc_state_obj == []:
        abort(404)
    return jsonify(loc_state_obj[0])


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """This Function Deletes a State object"""
    loc_all_states = storage.all("State").values()
    loc_state_obj = [obj.to_dict() for obj in loc_all_states if obj.id == state_id]
    if loc_state_obj == []:
        abort(404)
    loc_state_obj.remove(loc_state_obj[0])
    for obj in loc_all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"])
def create_state():
    """This Function Creates a State"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    loc_states = []
    loc_new_state = State(name=request.json["name"])
    storage.new(loc_new_state)
    storage.save()
    loc_states.append(loc_new_state.to_dict())
    return jsonify(loc_states[0]), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def updates_state(state_id):
    """This Function Updates a State object"""
    loc_all_states = storage.all("State").values()
    loc_state_obj = [obj.to_dict() for obj in loc_all_states if obj.id == state_id]
    if loc_state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    loc_state_obj[0]["name"] = request.json["name"]
    for obj in loc_all_states:
        if obj.id == state_id:
            obj.name = request.json["name"]
    storage.save()
    return jsonify(loc_state_obj[0]), 200
