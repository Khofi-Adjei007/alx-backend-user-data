#!/usr/bin/env python3
"""
Initialization of the app_views Blueprint and import of view modules.
"""
from flask import Blueprint

# Create a Blueprint named 'app_views' with a URL prefix of '/api/v1'
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views to register routes with the Blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Load User data from file
User.load_from_file()
