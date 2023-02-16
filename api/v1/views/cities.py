#!/usr/bin/python3
""" Handles all default RestFul API actions for Cities """
from api.v1.views import app_views
from models.city import City
from models import storage
from models.state import State
from flask import abort, make_response, request, jsonify


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Get list of cities
    """
    cities = storage.get(City, state_id)
    if not cities:
        abort(404)
    cities_list = []
    
    for city in cities:
        cities_list.append(city.to_dict())
    return make_response(jsonify(cities_list), 200)


@app_views.route('/cities/<city_id>', methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """
    Get cities by id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Delete cities by id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a city object
    """
    cities = storage.get(City, state_id)
    if not cities:
        abort(404)

    if not request.json():
        abort(400, description="Not a JSON")

    if 'name' not in request.json():
        abort(400, description="Missing name")

    city = request.json()
    add_city = City(**city)
    storage.save()
    return make_response(jsonify(add_city.to_dict()), 201)


@app_views.route(' /cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City by city_id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.json():
        abort(400, description="Not a JSON")

    if 'name' not in request.json():
        abort(400, description="Missing name")

    add_city = request.json()
    ignore = ["id", "state_id", "created_at", "updated_at"]

    for key, value in add_city.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
