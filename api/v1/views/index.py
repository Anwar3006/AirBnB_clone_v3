#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
import models

@app_views.route('/status', strict_slashes=False)
def status():
    """that returns a JSON of status code
    """
    return jsonify({"status": "OK"}), 200

@app_views.route('/api/v1/stats', strict_slashes=False)
def count():
    """
    Retrieves the number of each objects by type
    """
    return models.storage.count()