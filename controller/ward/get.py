from flask import Blueprint, request, jsonify, current_app
from crud.ward.get import get_ward_crud, get_wards_crud
from schemas.ward import WardResponse, WardListResponse
from sqlalchemy.exc import IntegrityError
from auth import require_auth

ward_get_bp = Blueprint("ward_get_bp", __name__ , url_prefix=("/ward"))

#Get Ward
@ward_get_bp.route("/get", methods=["GET"])
@require_auth
def get_ward():
    data = request.json
    id = data.get("id")

    if not id:
        current_app.logger.error(f"Wrong ward ID {id} provided.")
        return jsonify({
            "code": "WRONG_WARD_ID_PROVIDED",
            "message": f"Please enter correct ward ID."
        }), 403
    
    ward = get_ward_crud(id=id)

    try:
        if ward:
            current_app.logger.info(f"Ward '{ward}' response returned.")
            return WardResponse(ward).to_dict()
        
        else:
            current_app.logger.error(f"Ward ID {id} is not registered.")
            return jsonify({
                "code":"WARD_ID_DOESNT_EXIST",
                "message": f"Ward ID {id} is not registered, please try another."
            }), 403
    
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

#Get Wards
@ward_get_bp.route("/all", methods=["GET"])
@require_auth
def get_wards():

    try:
        wards = get_wards_crud()

        if wards:
            current_app.logger.info(f"Wards '{wards}' response returned.")
            return WardListResponse.from_list(wards) 
        else:
            current_app.logger.error("No wards found.")
            return jsonify({
                "code":"NO_WARDS_FOUND",
                "message":"No wards found, please add ward first."
            })
    
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