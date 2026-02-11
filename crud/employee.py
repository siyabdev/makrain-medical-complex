from flask import current_app
from database import db
from models.employee import Employee
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format, get_employee

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
    
#Get Employee
def get_employee_crud(id):
    try:
        employee = get_employee(id)
        return employee
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get Employees
def get_employees_crud():
    try:
        employees = Employee.query.all()
        db.session.commit()
        return employees
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get Short Details (Employees)
def get_employees_short_crud():
    try:
        employees = Employee.query.with_entities(Employee.id, Employee.employee_name, Employee.employee_role, Employee.employee_gender).all()
        db.session.commit()
        return employees
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

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
