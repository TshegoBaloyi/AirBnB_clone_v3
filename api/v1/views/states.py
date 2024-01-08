#!/usr/bin/python3
"""
This Handles all RESTful API actions for `State` objects.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states")
def states():
    """This Function Retrieve the list of all `State` objects"""
    locresult = []
    for value in storage.all(State).values():
        locresult.append(value.to_dict())
    return jsonify(locresult)


@app_views.route("/states/<state_id>")
def state(state_id: str):
    """This function Retrive one state object."""
    locresult = storage.get(State, state_id)
    if locresult is None:
        abort(404)
    return jsonify(locresult.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """This Function Delete a state object."""
    locstate = storage.get(State, state_id)
    if locstate is None:
        abort(404)
    locstate.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"])
def create_state():
    """This Function Create a `State` object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """This function Update `State` object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    key = "name"
    setattr(state, key, request.get_json().get(key))
    state.save()
    return jsonify(state.to_dict())
