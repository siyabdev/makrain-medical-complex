from flask import current_app
from database import db
from models.models import Employee
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format

#Create Employee
def create_employee_crud(ward_id, employee_code, employee_name, employee_role, employee_gender):

    try:
        create_query = Employee(
            ward_id = ward_id,
            employee_code = employee_code,
            employee_name = employee_name,
            employee_role = check_enum_format(employee_role),
            employee_gender = check_enum_format(employee_gender)
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