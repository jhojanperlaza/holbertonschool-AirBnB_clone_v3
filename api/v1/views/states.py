#!/usr/bin/python3
"""
retrieve an object into a valid JSON
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_obj = storage.all(State)
    lista = []
    for obj in all_obj.values():
        lista.append(obj.to_dict())
    return jsonify(lista)

@app_views.route('states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states_id(state_id):
    """Retrieves the list of all State objects with id"""
    linked_states = storage.get(State, state_id)
    if linked_states:
        return jsonify(linked_states.to_dict())
    else:
        abort(404)


@app_views.route('states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_states(state_id):
    """Deletes a state"""
    linked_states = storage.get(State, state_id)
    if linked_states:
        storage.close()
        storage.delete(linked_states)
        return {}, 200
    else:
        abort(404)
