#!/usr/bin/python3
"""Handles the default RESTful API actions for Users"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def get_users():
    """
    Get a list of users
    """
    users = storage.all(User)
    if not users:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    Get users by id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    Delete user by id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """
    Create user
    """
    if not request.json():
        abort(400, description="Not a JSON")
    if 'email' not in request.json():
        abort(400, description="Missing email")
    if 'password' not in request.json():
        abort(400, description="Missing password")

    new_user = request.json()
    user_object = User(**new_user)
    storage.save()
    return make_response(jsonify(user_object.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Updates user by id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    if not request.json():
        abort(400, description="Not a JSON")
    if 'password' not in request.json():
        abort(400, description="Missing password")
    
    ignore = ["id", "email", "created_at", "updated_at"]
    update = request.json()
    for key, value in update.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
