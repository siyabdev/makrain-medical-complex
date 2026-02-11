from flask import Blueprint, request, jsonify, current_app
from crud.ward import create_ward_crud, delete_ward_crud, get_ward_crud, get_wards_crud, update_ward_crud
from utils.utils import verify_ward, get_ward
from sqlalchemy.exc import IntegrityError
from schemas.ward import CreateWardRequest, DeleteWardRequest, WardResponse, WardListResponse, UpdateWardRequest
from auth import require_auth

#Blueprint
ward_bp = Blueprint("ward_bp", __name__ , url_prefix=("/ward"))

#Create Ward
@ward_bp.route("/create", methods=["POST"])
@require_auth
def create_ward_controller():
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

#Delete Ward
@ward_bp.route("/delete", methods=["DELETE"])
@require_auth
def delete_ward_controller():
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

#Get Ward
@ward_bp.route("/get", methods=["GET"])
@require_auth
def get_ward_controller():
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
@ward_bp.route("/all", methods=["GET"])
@require_auth
def get_wards_controller():

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
    
#Update Ward
@ward_bp.route("/update", methods=["PUT"])
@require_auth
def update_ward_controller():
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