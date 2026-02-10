from flask import Blueprint, request, jsonify, current_app
from crud.employee.create import create_employee_crud
from utils.utils import verify_employee
from sqlalchemy.exc import IntegrityError
from schemas.employee import CreateEmployeeRequest, EmployeeResponse
from auth import require_auth

employee_create_bp = Blueprint("employee_create_bp", __name__ , url_prefix="/employee")

#Create Employee
@employee_create_bp.route("/create", methods=["POST"])
@require_auth
def create_employee():
    data = CreateEmployeeRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    employee = verify_employee(data.employee_code, data.employee_name)

    if employee:
        current_app.logger.info(f"Employee already exists '{employee}'.")
        return jsonify({
            "code": "EMPLOYEE_ALREADY_EXISTS",
            "message": f"This employee '{employee}' already exists, try a new one."
        }), 403
    
    try:
        new_employee = create_employee_crud(
            ward_id = data.ward_id,
            employee_code = data.employee_code,
            employee_name = data.employee_name,
            employee_role = data.employee_role,
            employee_gender = data.employee_gender
        )

        current_app.logger.info(f"Employee {new_employee} created.")
        return jsonify({
            "code": "EMPLOYEE_CREATED",
            "data": EmployeeResponse(new_employee).to_dict()
        }), 201
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        return jsonify({
            "code": "INTEGRITY_ERROR",
            "message": f"Integrity error occured {error}."
        }), 409

    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        return jsonify({
            "code": "EXCEPTIONAL_ERROR",
            "message": f"Exceptional error occured {e}."
        }), 500