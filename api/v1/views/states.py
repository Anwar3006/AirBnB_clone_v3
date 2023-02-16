#!/usr/bin/python3
""" Handles all default RestFul API actions for States """
from api.v1.views import app_views
from models.base_model import BaseModel
import models
from models.state import State
from flask import make_response, request, jsonify, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    states = models.storage.all(State).values()
    
    list_state = []
    for state in states:
        list_state.append(state.to_dict())
    return jsonify(list_state)

@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """
    Retrieves a State object by id
    """
    state = models.storage.get(State, state_id)

    if not state:
        abort(404)
    
    return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object
    """
    state = models.storage.get(State, state_id)

    if not state:
        abort(404)

    models.storage.delete(state)
    models.storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create a State
    """
    if not request.json():
        abort(400, description="Not a JSON")

    if not 'name' in request.json:
        abort(400, description="Missing name")

    data = request.json()
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Update State by state_id
    """
    state = models.storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json():
        abort(400, description="Not a JSON")

    state['name'] = request.json()['name']
    models.storage.save()
    return make_response(jsonify(state.to_dict()), 200)
    
