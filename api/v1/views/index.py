#!/usr/bin/python3
"""This script contains blueprints for the application"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    """Returns the status of the API"""
    return jsonify({
        "status": "OK"
        })
