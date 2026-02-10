from flask import current_app
from database import db
from utils.utils import get_patient
from models.models import Patient
from sqlalchemy.exc import IntegrityError

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