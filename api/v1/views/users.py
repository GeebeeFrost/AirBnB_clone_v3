#!/usr/bin/python3
"""This script contains an app view for Amenity objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users(user_id=None):
    """
    If user_id is not provided, Retrieves a list of all User objects
    or Creates a new one depending on the request method.
    If user_id is provided, Retrieves, Edits or Deletes
    the specific User object depending on the request method
    """
    # /users
    if not user_id:
        if request.method == 'GET':
            all_users = storage.all(User).values()
            users_list = [user.to_dict() for user in all_users]
            return jsonify(users_list)
        if request.method == 'POST':
            if not request.get_json():
                abort(400, description="Not a JSON")
            if 'email' not in request.get_json():
                abort(400, description="Missing email")
            if 'password' not in request.get_json():
                abort(400, description="Missing password")
            user_data = request.get_json()
            new = User(**user_data)
            new.save()
            return jsonify(new.to_dict()), 201
    # /users/<user_id>
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")
        ignore = ["id", "email", "created_at", "updated_at"]
        user_data = request.get_json()
        for k, v in user_data.items():
            if k not in ignore:
                setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200
