#!/usr/bin/python3
"""Amenity file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    amenity_lst = []
    for key, value in storage.all(Amenity).items():
        return jsonify(amenity_lst(amenity_lst.append(value.to_dict())))


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity."""
    if request.content_type != 'application/json':
        return abort(400, description="Not a JSON")
    if not request.get_json():
        return abort(400, description="Not a JSON")
    amenity_data = request.get_json()
    if 'name' not in amenity_data():
        return abort(400, description="Missing name")
    new_amenity = Amenity(**amenity_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object."""
    if request.content_type != 'application/json':
        return abort(400, description="Not a JSON")
    if not request.get_json():
        return abort(400, description="Not a JSON")
    amenity_data = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        attr_keys = ['id', 'created_at', 'updated_at']
        for key, value in amenity_data.items():
            if key not in attr_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        return abort(404)
