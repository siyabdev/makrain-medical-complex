from flask import Blueprint, request, jsonify, current_app
from crud.patient.update import update_patient_crud
from utils.utils import get_patient
from sqlalchemy.exc import IntegrityError
from schemas.patient import UpdatePatientRequest, PatientResponse
from auth import require_auth

patient_update_bp = Blueprint("patient_update_bp", __name__ , url_prefix="/patient")

#Update Patient
@patient_update_bp.route("/update", methods=["PUT"])
@require_auth
def update_patient():
    data = UpdatePatientRequest(request.json)
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
    
    patient = get_patient(data.id)

    if not patient:
        current_app.logger.error(f"Patient ID '{patient}' not found.")
        return jsonify({
            "code": "PATIENT_NOT_FOUND", 
            "message": f"Patient ID '{patient}' not found."
        }), 404
    
    try:
        updated_patient = update_patient_crud(id=data.id, patient_name=data.patient_name, patient_gender=data.patient_gender, patient_age=data.patient_age)
        current_app.logger.info(f"Patient updated {updated_patient}.")
        return jsonify({
            "code": "PATIENT_UPDATED",
            "data": PatientResponse(updated_patient).to_dict()
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