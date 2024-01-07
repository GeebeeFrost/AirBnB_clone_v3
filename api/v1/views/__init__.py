#!/usr/bin/python3
"""This file allows for importing of views package"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
