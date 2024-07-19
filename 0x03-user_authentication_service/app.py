#!/usr/bin/env python3

"""A simple Flask application providing
user authentication functionalities.
"""

import logging
from flask import Flask, abort, jsonify, redirect, request
from auth import Auth


# Disable logging of warnings
logging.disable(logging.WARNING)


# Initialize the Auth class and Flask application
AUTH = Auth()
app = Flask(__name__)

@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """Handles GET requests to the root URL.
    
    Returns:
        JSON response containing a welcome message.
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Handles user registration.

    Returns:
        JSON response indicating success or failure of user registration.
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Handles user login.

    Returns:
        JSON response indicating success or failure of user login.
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """Handles user logout.

    Returns:
        Redirect to the home page if logout is successful.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")

@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Displays the user's profile.

    Returns:
        JSON response containing the user's email.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})

@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """Generates a password reset token.

    Returns:
        JSON response containing the email and reset token.
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)

@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Updates the user's password.

    Returns:
        JSON response indicating success of the password update.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
