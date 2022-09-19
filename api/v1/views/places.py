#!/usr/bin/python3
"""
retrieve an object into a valid JSON
"""

from models.place import Place
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('cities/<city_id>/places', strict_slashes=False)
def get_place(city_id):
    """Retrieves the list of all State objects"""
    linked_city = storage.get(City, city_id)
    if linked_city:
        all_obj = storage.all(Place)
        lista = []
        for obj in all_obj.values():
            if obj.city_id == city_id:
                lista.append(obj.to_dict())
        return jsonify(lista)
    else:
        abort(404)


@app_views.route('places/<place_id>', methods=['GET'])
def get_place_id(place_id):
    """Retrieves the list of all Amenity objects with id"""
    linked_place = storage.get(Place, place_id)
    if linked_place:
        return jsonify(linked_place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Deletes a User"""
    linked_user = storage.get(Place, place_id)
    if linked_user:
        storage.delete(linked_user)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ Creates a User object """
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")
    user_id = new_place['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in new_place:
        return ("Missing name"), 400

    linked_places = storage.get(City, city_id)
    if linked_places:
        user = User(**new_place)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'user_id', 'city_at',
                     'created_at', 'updated_at']:
            setattr(place, k, v)

    storage.save()
    return jsonify(place.to_dict()), 200