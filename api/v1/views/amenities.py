#!/usr/bin/python3
""" Handles all default RestFul API actions for Cities """
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, make_response, request, jsonify


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Get list of amenities
    """
    amenities = storage.all(Amenity)
    if not amenities:
        abort(404)
    return amenities.to_dict()


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Get amenities by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete amenity by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Create amenity
    """
    if not request.json():
        abort(400, description="Not a JSON")
    if 'name' not in request.json():
        abort(400, description="Missing name")

    new_amenity = request.json()
    amenity_instance = Amenity(**new_amenity)
    amenity_instance.save()
    return make_response(jsonify(amenity_instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update amenity by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json():
        abort(400, description="Not a JSON")
    if 'name' not in request.json():
        abort(400, description="Missing name")

    update = request.json()
    ignore = ["id", "created_at", "updated_at"]

    for key, value in update.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
