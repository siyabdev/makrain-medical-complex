from flask import current_app
from database import db
from utils.utils import get_ward
from models.models import Ward
from sqlalchemy.exc import IntegrityError

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