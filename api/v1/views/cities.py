#!/usr/bin/python3
"""
retrieve an object into a valid JSON
"""

from api.v1.views import app_views
from models import storage
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities')
def get_citys(state_id):
    """Retrieves the list of all State objects"""
    all_obj = storage.all(City)
    linked_states = storage.get(City.state_id, state_id)
    if linked_states:
        lista = []
        for obj in all_obj.values():
            lista.append(obj.to_dict())
        return jsonify(lista)
    else:
        abort(404)
