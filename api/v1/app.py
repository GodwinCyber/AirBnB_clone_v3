#!/usr/bin/python3
"""Create a variable app, instance of Flask"""
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(error):
    """Returns JSON error repsponse"""
    repsponse = {'error': 'Not found'}
    return jsonify(repsponse), 404


@app.teardown_appcontext
def close_storage(exception):
    """Call storage.close() after each request."""
    storage.close()


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', '5000'))
    app.run(debug=True, host=HOST, port=PORT, threaded=True)
