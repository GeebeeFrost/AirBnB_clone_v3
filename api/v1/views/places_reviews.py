#!/usr/bin/python3
"""This script contains an app view for Review objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route(
        "/places/<place_id>/reviews", methods=['GET', 'POST'],
        strict_slashes=False)
def add_get_reviews(place_id):
    """
    Retrieves the list of all Review objects linked to a Place object or
    Creates a new Review object linked to a Place object
    depending on the request method.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        reviews_list = [review.to_dict() for review in place.reviews]
        return jsonify(reviews_list)

    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")
        if 'user_id' not in request.get_json():
            abort(400, description="Missing user_id")
        if 'text' not in request.get_json():
            abort(400, description="Missing text")
        review_data = request.get_json()
        user = storage.get(User, review_data["user_id"])
        if not user:
            abort(404)
        new = Review(**review_data)
        new.place_id = place_id
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def get_delete_update_review(review_id):
    """
    Retrieves, Deletes or Updates a specific Review object
    depending on the request method
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")
        ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
        review_data = request.get_json()
        for k, v in review_data.items():
            if k not in ignore:
                setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200
