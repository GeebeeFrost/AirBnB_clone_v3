#!/usr/bin/python3
"""This script contains an app view for State objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """Retrieves the list of all State objects. If state_id is provided,
    retrieves the specific State object"""
    if not state_id:
        all_states = storage.all(State).values()
        states_list = [state.to_dict() for state in all_states]
        return jsonify(states_list)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
        "/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def add_edit_state(state_id=None):
    """Creates a new State object. If state_id is provided,
    makes changes to the specific State object"""
    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'name' not in request.get_json():
            abort(400, description="Missing name")
        state_data = request.get_json()
        new = State(**state_data)
        new.save()
        return jsonify(new.to_dict()), 201
    if request.method == 'PUT':
        if state_id:
            state = storage.get(State, state_id)
            if not state:
                abort(404)
            if not request.get_json():
                abort(400, description="Not a JSON")
            ignore = ["id", "created_at", "updated_at"]
            state_data = request.get_json()
            for k, v in state_data.items():
                if k not in ignore:
                    setattr(state, k, v)
            storage.save()
            return jsonify(state.to_dict()), 200
