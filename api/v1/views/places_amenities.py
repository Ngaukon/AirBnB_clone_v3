#!/usr/bin/python3
"""
Route for handling place and amenities linking.
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    Retrieves all amenities of a place.
    :param place_id: ID of the place
    :return: JSON list of all amenities for the specified place
    """
    fetched_obj = storage.get("Place", str(place_id))

    if fetched_obj is None:
        abort(404)

    all_amenities = [obj.to_json() for obj in fetched_obj.amenities]

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlinks an amenity from a place.
    :param place_id: ID of the place
    :param amenity_id: ID of the amenity
    :return: Empty JSON dictionary on success, or 404 on error
    """
    fetched_place = storage.get("Place", str(place_id))
    fetched_amenity = storage.get("Amenity", str(amenity_id))

    if fetched_place is None or fetched_amenity is None:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if fetched_amenity in fetched_place.amenities:
            fetched_place.amenities.remove(fetched_amenity)
        else:
            abort(404)
    else:
        if amenity_id in fetched_place.amenity_ids:
            fetched_place.amenity_ids.remove(amenity_id)
        else:
            abort(404)

    fetched_place.save()

    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links an amenity to a place.
    :param place_id: ID of the place
    :param amenity_id: ID of the amenity
    :return: JSON of the linked Amenity object, or error
    """
    fetched_place = storage.get("Place", str(place_id))
    fetched_amenity = storage.get("Amenity", str(amenity_id))

    if fetched_place is None or fetched_amenity is None:
        abort(404)

    if fetched_amenity in fetched_place.amenities:
        return jsonify(fetched_amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetched_place.amenities.append(fetched_amenity)
    else:
        fetched_place.amenities = fetched_amenity

    fetched_place.save()

    resp = jsonify(fetched_amenity.to_json())
    resp.status_code = 201

    return resp
