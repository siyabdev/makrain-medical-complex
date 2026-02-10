from flask import Blueprint, request, jsonify, current_app
from crud.employee.update import update_employee_crud
from utils.utils import get_employee
from sqlalchemy.exc import IntegrityError
from schemas.employee import UpdateEmployeeRequest, EmployeeResponse
from auth import require_auth

employee_update_bp = Blueprint("employee_update_bp", __name__ , url_prefix="/employee")

#Update Employee
@employee_update_bp.route("/update", methods=["PUT"])
@require_auth
def update_employee():
    data = UpdateEmployeeRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    if not data.has_any_updates():
        current_app.logger.error("Data missing.")
        return jsonify({
            "code": "DATA_MISSING", 
            "message": "Required fields for data update are not provided."
        }), 400
    
    employee = get_employee(data.id)

    if not employee:
        current_app.logger.error(f"Employee ID '{employee}' not found.")
        return jsonify({
            "code": "EMPLOYEE_NOT_FOUND", 
            "message": f"Employee ID '{employee}' not found."
        }), 404
    
    try:
        updated_employee = update_employee_crud(id=data.id, employee_name=data.employee_name, employee_role=data.employee_role, employee_gender=data.employee_gender)
        current_app.logger.info(f"Employee updated {updated_employee}.")
        return jsonify({
            "code": "EMPLOYEE_UPDATED",
            "data": EmployeeResponse(updated_employee).to_dict()
        }), 200
        
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