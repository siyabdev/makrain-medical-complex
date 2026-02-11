from flask import Blueprint, request, jsonify, current_app
from crud.patient import create_patient_crud, delete_patient_crud, get_patient_crud, get_patients_crud, get_patients_short_crud, update_patient_crud
from utils.utils import verify_patient, get_patient
from sqlalchemy.exc import IntegrityError
from schemas.patient import CreatePatientRequest, DeletePatientRequest, PatientResponse, PatientListResponse, PatientShortResponse, UpdatePatientRequest
from auth import require_auth

#Blueprints
patient_bp = Blueprint("patient_bp", __name__ , url_prefix="/patient")

#Create Patient
@patient_bp.route("/create", methods=["POST"])
@require_auth
def create_patient_controller():
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

#Delete Patient
@patient_bp.route("/delete", methods=["DELETE"])
@require_auth
def delete_patient_controller():
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

#Get Patient
@patient_bp.route("/get", methods=["GET"])
@require_auth
def get_patient_controller():
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
@patient_bp.route("/all", methods=["GET"])
@require_auth
def get_patients_controller():

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
@patient_bp.route("/short", methods=["GET"])
@require_auth
def get_patients_short_controller():

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

#Update Patient
@patient_bp.route("/update", methods=["PUT"])
@require_auth
def update_patient_controller():
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