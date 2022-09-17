#!/usr/bin/python3
"""
retrieve an object into a valid JSON
"""

from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_citys(state_id):
    """Retrieves the list of all State objects"""
    all_obj = storage.all(City)
    linked_states = storage.get(State, state_id)
    if linked_states:
        lista = []
        for obj in all_obj.values():
            lista.append(obj.to_dict())
        return jsonify(lista)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_City_id(city_id):
    """Retrieves the list of all State objects with id"""
    linked_states = storage.get(City, city_id)
    if linked_states:
        return jsonify(linked_states.to_dict())
    else:
        abort(404)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_citys(city_id):
    """Deletes a state"""
    linked_states = storage.get(City, city_id)
    if linked_states:
        storage.delete(linked_states)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_citys(state_id):
    """transform the HTTP body request to a dictionary"""
    if not request.json:
        return ("Not a JSON"), 400
    if 'name' not in request.json:
        return ("Missing name"), 400
    linked_states = storage.get(State, state_id)
    if linked_states:
        data = request.json
        new_inst = City()
        for k, v in data.items():
            setattr(new_inst, k, v)
            setattr(new_inst, 'state_id', state_id)
        storage.new(new_inst)
        storage.save()
        return new_inst.to_dict(), 201
    else:
        abort(400)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_citys(city_id):
    """Update a name of state"""
    linked_city = storage.get(City, city_id)
    if linked_city:
        data = request.json
        if not data:
            return ("Not a JSON"), 400
        for k, v in data.items():
            setattr(linked_city, k, v)
            storage.save()
            return linked_city.to_dict(), 200
    else:
        abort(404)
