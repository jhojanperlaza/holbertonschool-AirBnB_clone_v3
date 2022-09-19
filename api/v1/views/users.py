#!/usr/bin/python3
"""
retrieve an object into a valid JSON
"""

from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False)
def get_User():
    """Retrieves the list of all State objects"""
    all_obj = storage.all(User)
    lista = []
    for obj in all_obj.values():
        lista.append(obj.to_dict())
    return jsonify(lista)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_User_id(user_id):
    """Retrieves the list of all Amenity objects with id"""
    linked_user = storage.get(User, user_id)
    if linked_user:
        return jsonify(linked_user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_User(user_id):
    """Deletes a User"""
    linked_user = storage.get(User, user_id)
    if linked_user:
        storage.delete(linked_user)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'])
def post_User():
    """ Creates a User object """
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")

    data = request.json
    new_inst = User()
    for k, v in data.items():
        setattr(new_inst, k, v)
        storage.new(new_inst)
        storage.save()
        return new_inst.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_User(user_id):
    """Update a name of amenity"""
    linked_user = storage.get(User, user_id)
    if linked_user:
        data = request.get_json(request)
        if not data:
            return ("Not a JSON"), 400
        for k, v in data.items():
            setattr(linked_user, k, v)
        storage.save()
        return linked_user.to_dict(), 200
    else:
        abort(404)
