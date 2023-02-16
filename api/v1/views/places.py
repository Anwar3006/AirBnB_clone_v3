#!/usr/bin/python3
"""Handles all default RESTful API actions for Places"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.place import Place
from models import storage

@app_views.route('/cities/<city_id>/places', methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """
    Get places by city_id
    """
    places = storage.get(Place, city_id)
    if not places:
        abort(404)
    places_list = []

    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    Get place by id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    Delete a place by id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/cities/<city_id>/places', methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """
    Create a place
    """
    places = storage.get(Place, city_id)
    if not places:
        abort(404)
    
    if not request.json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json():
        abort(400, description="Missing user_id")

    new_place = request.json()
    if new_place['user_id'] not in places:
        abort(404)

    place_object = Place(**new_place)
    storage.save()
    return make_response(jsonify(place_object.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates place by id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.json():
        abort(400, description="Not a JSON")
    
    update = request.json()
    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, value in update.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
    