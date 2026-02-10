from flask import current_app
from database import db
from models.models import Patient
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format

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