from flask import current_app
from database import db
from models.models import Ward
from sqlalchemy.exc import IntegrityError

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