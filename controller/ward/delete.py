from flask import Blueprint, request, jsonify, current_app
from crud.ward.delete import delete_ward_crud
from utils.utils import get_ward
from sqlalchemy.exc import IntegrityError
from schemas.ward import DeleteWardRequest
from auth import require_auth

ward_delete_bp = Blueprint("ward_delete_bp", __name__ , url_prefix=("/ward"))

#Delete Ward
@ward_delete_bp.route("/delete", methods=["DELETE"])
@require_auth
def delete_ward():
    data = DeleteWardRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    ward = get_ward(data.id)

    if not ward:
        current_app.logger.info(f"Ward ID '{ward}' doesnt exist.")
        return jsonify({
            "code": "WARD_DOESNT_EXIST",
            "message": f"Ward ID '{ward}' doesnt exist, please enter a valid ward ID."
        })
    
    try:
        delete_query = delete_ward_crud(id=data.id)
        if delete_query:
            current_app.logger.info(f"Ward ID {data.id} is deleted.")
            return jsonify({
                "code": "WARD_DELETED",
                "message": f"Ward ID {data.id} is deleted."
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