#!/usr/bin/python3
"""Create Flask: app_views"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returns status"""
    return jsonify({'status': 'OK'})
