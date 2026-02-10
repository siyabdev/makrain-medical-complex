from flask import Blueprint, request, jsonify, current_app
from crud.patient.delete import delete_patient_crud
from utils.utils import get_patient
from sqlalchemy.exc import IntegrityError
from schemas.patient import DeletePatientRequest
from auth import require_auth

patient_delete_bp = Blueprint("patient_delete_bp", __name__ , url_prefix="/patient")

#Delete Patient
@patient_delete_bp.route("/delete", methods=["DELETE"])
@require_auth
def delete_patient():
    data = DeletePatientRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    patient = get_patient(data.id)

    if not patient:
        current_app.logger.info(f"Patient ID '{patient}' doesnt exist.")
        return jsonify({
            "code": "PATIENT_DOESNT_EXIST",
            "message": f"Patient ID '{patient}' doesnt exist, please enter a valid patient ID."
        })
    
    try:
        delete_query = delete_patient_crud(id=data.id)
        if delete_query:
            current_app.logger.info(f"Patient ID {data.id} is deleted.")
            return jsonify({
                "code": "PATIENT_DELETED",
                "message": f"Patient ID {data.id} is deleted."
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