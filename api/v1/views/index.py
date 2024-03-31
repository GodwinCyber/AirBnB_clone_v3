#!/usr/bin/python3
"""Create Flask: app_views"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returns status"""
    return jsonify({'status': 'OK'})

@app_views.route("/stats", strict_slashes=False)
def stats():
    """Returns stats"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
