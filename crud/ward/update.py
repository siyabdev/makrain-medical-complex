from flask import current_app
from database import db
from utils.utils import get_ward
from sqlalchemy.exc import IntegrityError

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