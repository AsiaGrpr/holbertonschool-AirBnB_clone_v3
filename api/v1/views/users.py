#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """list all users"""

    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ select user by id"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete user by id"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """create user"""

    new_user = request.get_json(silent=True)
    if not new_user:
        return abort(400, {"Not a JSON"})

    if "email" not in new_user:
        return abort(400, {"Missing email"})

    if "password" not in new_user:
        return abort(400, {"Missing password"})

    new_obj = User(**new_user)
    new_obj.save()

    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update user by id"""

    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})

    old = storage.get(User, user_id)
    if not old:
        return abort(404)

    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in new.items():
        if key not in ignore:
            setattr(old, key, value)
    storage.save()
    return make_response(jsonify(old.to_dict()), 200)
