#!/usr/bin/env python3

"""
Route module for the API: Initializes and configures the Flask app, handles
authentication, and sets up error handlers and request validation.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os
from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

# Import and initialize the appropriate authentication class based on AUTH_TYPE
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()

@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handler for 404 Not Found errors.
    Returns a JSON response with an error message.
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """
    Handler for 401 Unauthorized errors.
    Returns a JSON response with an error message.
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_error(error) -> str:
    """
    Handler for 403 Forbidden errors.
    Returns a JSON response with an error message.
    """
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def before_request() -> str:
    """
    Before request handler that validates requests.
    Checks authentication and authorization before processing requests.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        abort(401)

    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)

    request.current_user = current_user

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
