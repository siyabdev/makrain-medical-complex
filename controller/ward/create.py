from flask import Blueprint, request, jsonify, current_app
from crud.ward.create import create_ward_crud
from utils.utils import verify_ward
from sqlalchemy.exc import IntegrityError
from schemas.ward import CreateWardRequest, WardResponse
from auth import require_auth

ward_create_bp = Blueprint("ward_create_bp", __name__ , url_prefix=("/ward"))

#Create Ward
@ward_create_bp.route("/create", methods=["POST"])
@require_auth
def create_ward():
    data = CreateWardRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    ward = verify_ward(data.ward_name, data.floor_number)

    if ward:
        current_app.logger.info(f"Ward already exists '{ward}'.")
        return jsonify({
            "code": "WARD_ALREADY_EXISTS",
            "message": f"This ward '{ward}' already exists, try a new one."
        }), 403
    
    try:
        new_ward = create_ward_crud(
            ward_name = data.ward_name,
            floor_number = data.floor_number
        )

        current_app.logger.info(f"Ward {new_ward} created.")
        return jsonify({
            "code": "WARD_CREATED",
            "data": WardResponse(new_ward).to_dict()
        }), 201
    
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