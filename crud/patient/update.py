from flask import current_app
from database import db
from utils.utils import get_patient, check_enum_format
from sqlalchemy.exc import IntegrityError

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