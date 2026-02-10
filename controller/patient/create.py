from flask import Blueprint, request, jsonify, current_app
from crud.patient.create import create_patient_crud
from utils.utils import verify_patient
from sqlalchemy.exc import IntegrityError
from schemas.patient import CreatePatientRequest, PatientResponse
from auth import require_auth

patient_create_bp = Blueprint("patient_create_bp", __name__ , url_prefix="/patient")

#Create Patient
@patient_create_bp.route("/create", methods=["POST"])
@require_auth
def create_patient():
    data = CreatePatientRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    patient = verify_patient(data.patient_code, data.patient_name)

    if patient:
        current_app.logger.info(f"Patient already exists '{patient}'.")
        return jsonify({
            "code": "PATIENT_ALREADY_EXISTS",
            "message": f"This patient '{patient}' already exists, try a new one."
        }), 403
    
    try:
        new_patient = create_patient_crud(
            ward_id = data.ward_id,
            patient_code = data.patient_code,
            patient_name = data.patient_name,
            patient_gender = data.patient_gender,
            patient_age = data.patient_age
        )

        current_app.logger.info(f"Patient {new_patient} created.")
        return jsonify({
            "code": "PATIENT_CREATED",
            "data": PatientResponse(new_patient).to_dict()
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