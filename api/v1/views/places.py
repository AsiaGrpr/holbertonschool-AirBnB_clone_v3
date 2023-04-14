#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places():
    """list all places"""

    all_places = storage.all(Place).values()
    list_places = []
    for place in all_places:
        list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ select place by id"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete user by id"""

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/places", methods=["POST"], strict_slashes=False)
def create_place():
    """create user"""

    new_place = request.get_json(silent=True)
    if not new_place:
        return abort(400, {"Not a JSON"})

    if "email" not in new_place:
        return abort(400, {"Missing email"})

    if "password" not in new_place:
        return abort(400, {"Missing password"})

    new_obj = User(**new_place)
    new_obj.save()

    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """update user by id"""

    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})

    old = storage.get(Place, place_id)
    if not old:
        return abort(404)

    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for key, value in new.items():
        if key not in ignore:
            setattr(old, key, value)
    storage.save()
    return make_response(jsonify(old.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def cities_places(city_id):
    """get places of a city"""

    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})
    
    if "user_id" not in new:
        return abort(400, {"Missing user_id"})
    
    user = storage.get(User, city.user_id)
    
    if not user:
        return abort(404)
    
    if "name" not in new:
        return abort(400, {"Missing name"})
    
    new_obj = Place(name=new_state['name'], city_id=city.id, user_id=user.id)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)

    
     
   