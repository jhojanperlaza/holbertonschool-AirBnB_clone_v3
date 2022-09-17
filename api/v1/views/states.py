#!/usr/bin/python3
"""
retrieve an object into a valid JSON
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


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
        storage.delete(linked_states)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_states():
    """transform the HTTP body request to a dictionary"""
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        return ("Missing name"), 400
    data = request.json
    new_inst = State()
    for k, v in data.items():
        setattr(new_inst, k, v)
    storage.new(new_inst)
    storage.save()
    return new_inst.to_dict(), 201


@app_views.route('states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_states(state_id):
    """Update a name of state"""
    linked_states = storage.get(State, state_id)
    if linked_states:
        data = request.json
        if not data:
            return ("Not a JSON"), 400
        for k, v in data.items():
            setattr(linked_states, k, v)
            storage.save()
            return linked_states.to_dict(), 200
    else:
        abort(404)
