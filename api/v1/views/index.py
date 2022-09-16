#!/usr/bin/python3
"""
initialize 
"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
app = app_views

@app.route('/status', strict_slashes=False)

def index():
    """returns returns a JSON: status: OK"""
    return jsonify("status: OK")
