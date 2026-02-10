from flask import Blueprint, request, jsonify, current_app
from crud.ward.update import update_ward_crud
from utils.utils import get_ward
from sqlalchemy.exc import IntegrityError
from schemas.ward import UpdateWardRequest, WardResponse
from auth import require_auth

ward_update_bp = Blueprint("ward_update_bp", __name__ , url_prefix="/ward")

#Update Ward
@ward_update_bp.route("/update", methods=["PUT"])
@require_auth
def update_ward():
    data = UpdateWardRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    if not data.has_any_updates():
        current_app.logger.error("Data missing.")
        return jsonify({
            "code": "DATA_MISSING", 
            "message": "Required fields for data update are not provided."
        }), 400
    
    ward = get_ward(data.id)

    if not ward:
        current_app.logger.error(f"Ward ID '{ward}' not found.")
        return jsonify({
            "code": "WARD_NOT_FOUND", 
            "message": f"Ward ID '{ward}' not found."
        }), 404
    
    try:
        updated_ward = update_ward_crud(id=data.id, ward_name=data.ward_name, floor_number=data.floor_number)
        current_app.logger.info(f"Ward updated {updated_ward}.")
        return jsonify({
            "code": "WARD_UPDATED",
            "data": WardResponse(updated_ward).to_dict()
        }), 200
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code": "EXCEPTIONAL_ERROR",
            "message": f"Exceptional error occured {e}."
        }), 500