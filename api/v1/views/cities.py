#!/usr/bin/python3
""" View for City objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities')
def get_citys(state_id):
    """Retrieves the list of all State objects"""
    linked_states = storage.get(State, state_id)
    if linked_states:
        lista = []
        for obj in linked_states.cities:
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


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_citys(state_id):
    """ Creates a City object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if "name" not in new_city:
        abort(400, "Missing name")
    data = request.json
    new_inst = City()
    for k, v in data.items():
        setattr(new_inst, k, v)
        setattr(new_inst, 'state_id', state_id)
        storage.new(new_inst)
        storage.save()
        return new_inst.to_dict(), 201


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
