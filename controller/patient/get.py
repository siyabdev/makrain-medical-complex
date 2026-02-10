from flask import Blueprint, request, jsonify, current_app
from crud.patient.get import get_patient_crud, get_patients_crud, get_patients_short_crud
from schemas.patient import PatientResponse, PatientListResponse, PatientShortResponse
from sqlalchemy.exc import IntegrityError
from auth import require_auth

patient_get_bp = Blueprint("patient_get_bp", __name__ , url_prefix="/patient")

#Get Patient
@patient_get_bp.route("/get", methods=["GET"])
@require_auth
def get_patient():
    data = request.json
    id = data.get("id")

    if not id:
        current_app.logger.error(f"Wrong patient ID {id} provided.")
        return jsonify({
            "code": "WRONG_PATIENT_ID_PROVIDED",
            "message": f"Please enter correct patient ID."
        }), 403
    
    patient = get_patient_crud(id=id)

    try:
        if patient:
            current_app.logger.info(f"Patient '{patient}' response returned.")
            return PatientResponse(patient).to_dict()
        
        else:
            current_app.logger.error(f"Patient ID {id} is not registered.")
            return jsonify({
                "code":"PATIENT_ID_DOESNT_EXIST",
                "message": f"Patient ID {id} is not registered, please try another."
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

#Get Patients
@patient_get_bp.route("/all", methods=["GET"])
@require_auth
def get_patients():

    try:
        patients = get_patients_crud()

        if patients:
            current_app.logger.info(f"Patients '{patients}' response returned.")
            return PatientListResponse.from_list(patients)
        else:
            current_app.logger.error("No patients found.")
            return jsonify({
                "code":"NO_PATIENTS_FOUND",
                "message":"No patients found, please add patient first."
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

#Get Short Details (Patients)
@patient_get_bp.route("/short", methods=["GET"])
@require_auth
def get_patients_short():

    try:
        patients = get_patients_short_crud()

        if patients:
            current_app.logger.info(f"Patients '{patients}' response returned.")
            return PatientShortResponse.from_list(patients)

        else:
            current_app.logger.error("No patients found")
            return jsonify({
                "code":"NO_PATIENTS_FOUND",
                "message":"No patients found, please add patient first."
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