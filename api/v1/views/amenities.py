#!/usr/bin/python3
"""Module for amenities object"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """list all amenities"""

    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())

    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """select amenity by id"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity by id"""

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create amenity"""

    new_amenity = request.get_json(silent=True)
    if not new_amenity:
        return abort(400, {"Not a JSON"})

    if "name" not in new_amenity.keys():
        return abort(400, {"Missing name"})

    new_obj = Amenity(name=new_amenity['name'])
    storage.new(new_obj)
    storage.save()

    return make_response(new_obj.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update amenity by id"""

    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})

    old = storage.get(Amenity, amenity_id)
    if not old:
        return abort(404)

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in new.items():
        if key not in ignore:
            setattr(old, key, value)
    storage.save()
    return make_response(jsonify(old.to_dict()), 200)
