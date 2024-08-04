#!/usr/bin/python3
"""
Routes for handling State objects and operations related to City objects.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City

@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    Retrieves all City objects in a specific state.
    :param state_id: ID of the state
    :return: JSON list of all cities in the state or 404 if state not found
    """
    city_list = []
    state_obj = storage.get("State", state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_json())

    return jsonify(city_list)

@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    Creates a new City object in a specific state.
    :param state_id: ID of the state
    :return: JSON of the newly created city object, or appropriate error code
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    resp = jsonify(new_city.to_json())
    resp.status_code = 201

    return resp

@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    Retrieves a specific City object by ID.
    :param city_id: ID of the city
    :return: JSON of the city object or 404 if not found
    """
    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())

@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    Updates a specific City object by ID.
    :param city_id: ID of the city
    :return: JSON of the updated city object, or appropriate error code
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())

@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    Deletes a specific City object by ID.
    :param city_id: ID of the city
    :return: Empty dictionary with status 200, or 404 if city not found
    """
    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
