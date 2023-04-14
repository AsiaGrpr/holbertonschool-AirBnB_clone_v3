#!/usr/bin/python3
"""Testing documentation of a module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_review(place_id):
    """Testing documentation of a module"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    else:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE'])
def get_review_id(review_id):
    """Testing documentation of a module"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    elif request.method == 'GET':
        review_id = review.to_dict()
        return jsonify(review_id)
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """Testing documentation of a module"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    create_review = request.get_json()
    if not create_review:
        abort(400, description="Not a JSON")
    elif 'user_id' not in create_review:
        abort(400, description="Missing user_id")
    elif 'text' not in create_review:
        abort(400, description="Missing text")
    create_review['place_id'] = place_id
    user = storage.get(User, create_review['user_id'])
    if not user:
        abort(404)
    new_Review = Review(**create_review)
    new_Review.save()
    return (jsonify(new_Review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Testing documentation of a module"""
    review = storage.get(Review, review_id)
    request_json = request.get_json()
    if request_json is None:
        abort(400, description="Not a JSON")
    if review is None:
        abort(404)
    for x, val in request_json.items():
        if x not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, x, val)
    storage.save()
    return jsonify(review.to_dict()), 200
