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


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_citys(state_id):
    """transform the HTTP body request to a dictionary"""
    new_city = request.get_json()
    if not new_city:
        return ("Not a JSON"), 400
    if 'name' not in request.json:
        return ("Missing name"), 400
    linked_states = storage.get(State, state_id)
    if linked_states:
        new_inst = City(**new_city)
        setattr(new_inst, 'state_id', state_id)
        storage.new(new_inst)
        storage.save()
        return  make_response(jsonify(new_inst.to_dict()), 201)
    else:
        abort(400)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """ Updates a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
