#!/usr/bin/python3
"""User file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects."""
    all_users = storage.all(User).values()
    return jsonify([user.to_dict() for user in all_users])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User."""
    if request.content_type != 'application/json':
        return abort(400, description="Not a JSON")
    if not request.get_json():
        return abort(400, description="Not a JSON")
    user_data = request.get_json()
    if 'email' not in user_data:
        return abort(400, description="Missing email")
    if 'password' not in user_data:
        return abort(400, description="Missing password")
    new_user = User(**user_data)
    new_user.new(new_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object."""
    user = storage.get(User, user_id)
    if not user:
        return abort(404)
    if not request.get_json():
        return abort(400, description="Not a JSON")
    if request.content_type != 'application/json':
        return abort(404, description="Not a JSON")
    user_data = request.get_json()
    for key, value in user_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
