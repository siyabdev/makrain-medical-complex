from flask import current_app
from database import db
from utils.utils import get_employee, check_enum_format
from sqlalchemy.exc import IntegrityError

#Update Employee
def update_employee_crud(id, employee_name, employee_role, employee_gender):
    employee = get_employee(id)

    if not employee:
        return employee == False
    try:
        #Update provided fields
        if employee_name:
            employee.employee_name = employee_name
        
        if employee_role:
            employee.employee_role = check_enum_format(employee_role)
        
        if employee_gender:
            employee.employee_gender = check_enum_format(employee_gender)

        db.session.commit()
        return employee
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
        
