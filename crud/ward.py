from flask import current_app
from database import db
from models.ward import Ward
from sqlalchemy.exc import IntegrityError
from utils.utils import get_ward

#Create Ward
def create_ward_crud(ward_name, floor_number):

    try:
        create_query = Ward(
            ward_name = ward_name,
            floor_number = floor_number
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

#Delete Ward
def delete_ward_crud(id):
    try:
        delete_query = Ward.query.filter_by(id=id).first()
        db.session.delete(delete_query)
        db.session.commit()

        return delete_query
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get Ward
def get_ward_crud(id):
    try:
        ward = get_ward(id)
        return ward
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get Wards
def get_wards_crud():
    try:
        wards = Ward.query.all()
        db.session.commit()
        return wards
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Update Ward
def update_ward_crud(id, ward_name, floor_number):
    ward = get_ward(id)

    if not ward:
        return ward == False
    try:
        #Update provided fields
        if ward_name:
            ward.ward_name = ward_name

        if floor_number:
            ward.floor_number = floor_number
        
        db.session.commit()
        return ward
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e