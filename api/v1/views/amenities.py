#!/usr/bin/python3
"""
retrieve an object into a valid JSON
"""

from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities')
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    all_obj = storage.all(Amenity)
    if all_obj:
        return jsonify(all_obj)
    else:
        abort(404)


@app_views.route('amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenities_id(amenity_id):
    """Retrieves the list of all Amenity objects with id"""
    linked_amenities = storage.get(Amenity, amenity_id)
    if linked_amenities:
        return jsonify(linked_amenities.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenities(amenity_id):
    """Deletes a amenity"""
    linked_amenities = storage.get(Amenity, amenity_id)
    if linked_amenities:
        storage.delete(linked_amenities)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'])
def post_amenities():
    """transform the HTTP body request to a dictionary"""
    if not request.get_json(request):
        return ("Not a JSON"), 400
    if 'name' not in request.get_json(request):
        return ("Missing name"), 400
    all_amenities = storage.all(Amenity)
    if all_amenities:
        data = request.get_json(request)
        new_inst = Amenity()
        for k, v in data.items():
            setattr(new_inst, k, v)
        storage.new(new_inst)
        storage.save()
        return new_inst.to_dict(), 201
    else:
        abort(400)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def put_amenities(amenity_id):
    """Update a name of amenity"""
    linked_amenities = storage.get(Amenity, amenity_id)
    if linked_amenities:
        data = request.get_json(request)
        if not data:
            return ("Not a JSON"), 400
        for k, v in data.items():
            setattr(linked_amenities, k, v)
        storage.save()
        return linked_amenities.to_dict(), 200
    else:
        abort(404)
