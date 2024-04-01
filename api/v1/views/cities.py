#!/usr/bin/python3
"""City file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State."""
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    city_list = [city.to_dict() for city in state.city_list]
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object."""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object."""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City in a State."""
    if request.content_type != 'application/json':
        return abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.get_json():
        return abort(400, description="Not a JSON")
    city_data = request.get_json()
    if 'name' not in city_data:
        return abort(400, description="Missing name")
    city_data['state_id'] = state_id
    new_city = City(**city_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return abort(400, description="Not a JSON")
    city_data = request.get_json()
    for key, value in city_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
