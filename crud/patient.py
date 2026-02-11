from flask import current_app
from database import db
from models.patient import Patient
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format, get_patient

#Create Patient
def create_patient_crud(ward_id, patient_code, patient_name, patient_gender, patient_age):

    try:
        create_query = Patient(
            ward_id = ward_id,
            patient_code = patient_code,
            patient_name = patient_name,
            patient_gender = check_enum_format(patient_gender),
            patient_age = patient_age
        )

        db.session.add(create_query)
        db.session.commit()

        return create_query
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Delete Patient
def delete_patient_crud(id):
    try:
        delete_query = Patient.query.filter_by(id=id).first()
        db.session.delete(delete_query)
        db.session.commit()

        return delete_query
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise

#Get Patient
def get_patient_crud(id):
    try:
        patient = get_patient(id)
        return patient
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
    
#Get Patients
def get_patients_crud():
    try:
        patients = Patient.query.all()
        db.session.commit()
        return patients
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
    
#Get Short Details (Patients)
def get_patients_short_crud():
    try:
        patients = Patient.query.with_entities(Patient.id, Patient.patient_name, Patient.patient_gender, Patient.patient_age).all()
        db.session.commit()
        return patients
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Update Patient
def update_patient_crud(id, patient_name, patient_gender, patient_age):
    patient = get_patient(id)

    if not patient:
        return patient == False
    try:
        #Update provided fields
        if patient_name:
            patient.patient_name = patient_name
        
        if patient_gender:
            patient.patient_gender = check_enum_format(patient_gender)
        
        if patient_age:
            patient.patient_age = patient_age
        
        db.session.commit()
        return patient
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e