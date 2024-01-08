#!/usr/bin/python3
"""This script contains an app view for Amenity objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities(amenity_id=None):
    """
    If amenity_id is not provided, Retrieves a list of all Amenity objects
    or Creates a new one depending on the request method.
    If amenity_id is provided, Retrieves, Edits or Deletes
    the specific Amenity object depending on the request method
    """
    # /amenities
    if not amenity_id:
        if request.method == 'GET':
            all_amenities = storage.all(Amenity).values()
            amenities_list = [amenity.to_dict() for amenity in all_amenities]
            return jsonify(amenities_list)
        if request.method == 'POST':
            if not request.get_json():
                abort(400, description="Not a JSON")
            if 'name' not in request.get_json():
                abort(400, description="Missing name")
            amenity_data = request.get_json()
            new = Amenity(**amenity_data)
            new.save()
            return jsonify(new.to_dict()), 201
    # /amenities/<amenity_id>
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")
        ignore = ["id", "created_at", "updated_at"]
        amenity_data = request.get_json()
        for k, v in amenity_data.items():
            if k not in ignore:
                setattr(amenity, k, v)
        storage.save()
        return jsonify(amenity.to_dict()), 200
