#!/usr/bin/python3
"""This script contains an app view for City objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        "/states/<state_id>/cities", methods=['GET', 'POST'],
        strict_slashes=False)
def add_get_cities(state_id):
    """Retrieves the list of all City objects linked to a State object or
    Creates a new City object linked to a State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        cities_list = [city.to_dict() for city in state.cities]
        return jsonify(cities_list)
    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'name' not in request.get_json():
            abort(400, description="Missing name")
        city_data = request.get_json()
        new = City(**city_data)
        new.state_id = state_id
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
        "/cities/<city_id>", methods=['GET', 'DELETE'], strict_slashes=False)
def get_delete_city(city_id):
    """Retrieves or Deletes a City object"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def edit_city(city_id=None):
    """Makes changes to a specific City object"""
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        if not request.get_json():
            abort(400, description="Not a JSON")
        ignore = ["id", "state_id", "created_at", "updated_at"]
        city_data = request.get_json()
        for k, v in city_data.items():
            if k not in ignore:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200
