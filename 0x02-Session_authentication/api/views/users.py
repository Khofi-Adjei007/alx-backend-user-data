#!/usr/bin/env python3
"""
Module for User views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    Handle GET requests to /api/v1/users.
    
    Returns:
        - JSON list of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    Handle GET requests to /api/v1/users/<user_id>.
    
    Args:
        user_id (str): The ID of the User to retrieve.
        
    Returns:
        - JSON representation of the User object.
        - 404 error if the User ID does not exist.
    """
    if user_id is None:
        abort(404)

    if user_id == "me" and request.current_user is None:
        abort(404)

    if user_id == "me" and request.current_user is not None:
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    Handle DELETE requests to /api/v1/users/<user_id>.
    
    Args:
        user_id (str): The ID of the User to delete.
        
    Returns:
        - Empty JSON dictionary if the User was deleted successfully.
        - 404 error if the User ID does not exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    Handle POST requests to /api/v1/users.
    
    JSON body:
        - email (required)
        - password (required)
        - last_name (optional)
        - first_name (optional)
        
    Returns:
        - JSON representation of the newly created User object.
        - 400 error if the User could not be created.
    """
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None

    if rj is None:
        return jsonify({'error': "Wrong format"}), 400
    if rj.get("email", "") == "":
        return jsonify({'error': "email missing"}), 400
    if rj.get("password", "") == "":
        return jsonify({'error': "password missing"}), 400
    
    try:
        user = User()
        user.email = rj.get("email")
        user.password = rj.get("password")
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    Handle PUT requests to /api/v1/users/<user_id>.
    
    Args:
        user_id (str): The ID of the User to update.
        
    JSON body:
        - last_name (optional)
        - first_name (optional)
        
    Returns:
        - JSON representation of the updated User object.
        - 404 error if the User ID does not exist.
        - 400 error if the User could not be updated.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    
    try:
        rj = request.get_json()
    except Exception as e:
        rj = None

    if rj is None:
        return jsonify({'error': "Wrong format"}), 400

    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
