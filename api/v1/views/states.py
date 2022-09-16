#!/usr/bin/python3
"""
retrieve an object into a valid JSON
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_obj = storage.all(State)
    lista = []
    for obj in all_obj.values():
        lista.append(obj.to_dict())
    return jsonify(lista)

@app_views.route('/states', strict_slashes=False)
def get_states_id():
    """Retrieves the list of all State objects with id"""
    all_obj = storage.all(State)
    lista = []
    for obj in all_obj.values():
        lista.append(obj.to_dict())
    return jsonify(lista)
