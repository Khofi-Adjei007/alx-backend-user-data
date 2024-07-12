#!/usr/bin/env python3
"""
Module for Session Authentication views.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handle POST requests to /auth_session/login.
    
    This function logs in a user by creating a session if the provided email
    and password are correct.
    
    Returns:
        - JSON response with the logged-in user's information if successful.
        - JSON error message if email or password is missing or incorrect.
    """
    email = request.form.get('email')

    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        found_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not found_users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in found_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user = found_users[0]
    session_id = auth.create_session(user.id)

    SESSION_NAME = getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Handle DELETE requests to /auth_session/logout.
    
    This function logs out a user by destroying the session.
    
    Returns:
        - Empty JSON dictionary if successful.
        - 404 error if the session could not be destroyed.
    """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
