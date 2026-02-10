from flask import current_app
from database import db
from models.models import Employee
from sqlalchemy.exc import IntegrityError

#Delete Employee
def delete_employee_crud(id):
    try:
        delete_query = Employee.query.filter_by(id=id).first()
        db.session.delete(delete_query)
        db.session.commit()

        return delete_query
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e