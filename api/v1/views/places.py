#!/usr/bin/python3
"""Place file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place in a City."""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    if not request.get_json():
        return abort(400, description="Not a JSON")
    place_data = request.get_json()
    if 'user_id' not in place_data:
        return abort(400, description="Missing user_id")
    if 'name' not in place_data:
        return abort(400, description="Missing name")
    user = storage.get(User, place_data['user_id'])
    if not user:
        return abort(404)
    place_data['city_id'] = city_id
    new_place = Place(**place_data)
    new_place.new(new_place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return abort(400, description="Not a JSON")
    place_data = request.get_json()
    for key, value in place_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
