from flask import Blueprint, request, jsonify, current_app
from crud.employee.get import get_employee_crud, get_employees_crud, get_employees_short_crud
from schemas.employee import EmployeeResponse, EmployeeListResponse, EmployeeShortResponse
from sqlalchemy.exc import IntegrityError
from auth import require_auth

employee_get_bp = Blueprint("employee_get_bp", __name__ , url_prefix="/employee")

#Get Employee
@employee_get_bp.route("/get", methods=["GET"])
@require_auth
def get_employee():
    data = request.json
    id = data.get("id")

    if not id:
        current_app.logger.error(f"Wrong employee ID {id} provided.")
        return jsonify({
            "code": "WRONG_EMPLOYEE_ID_PROVIDED",
            "message": f"Please enter correct employee ID."
        }), 403
    
    employee = get_employee_crud(id=id)

    try:
        if employee:
            current_app.logger.info(f"Employee '{employee}' response returned.")
            return EmployeeResponse(employee).to_dict()
        
        else:
            current_app.logger.error(f"Employee ID {id} is not registered.")
            return jsonify({
                "code":"EMPLOYEE_ID_DOESNT_EXIST",
                "message": f"Employee ID {id} is not registered, please try another."
            }), 403
        
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

#Get Employees
@employee_get_bp.route("/all", methods=["GET"])
@require_auth
def get_employees():

    try:
        employees = get_employees_crud()

        if employees:
            current_app.logger.info(f"Employees '{employees}' response returned.")
            return EmployeeListResponse.from_list(employees) 
        else:
            current_app.logger.error("No employees found.")
            return jsonify({
                "code":"NO_EMPLOYEES_FOUND",
                "message":"No employees found, please add employee first."
            })
        
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
    
#Get Short Details (Employees)
@employee_get_bp.route("/short", methods=["GET"])
@require_auth
def get_employees_short():

    try:
        employees = get_employees_short_crud()

        if employees:
            current_app.logger.info(f"Employees '{employees}' response returned.")
            return EmployeeShortResponse.from_list(employees)

        else:
            current_app.logger.error("No employees found")
            return jsonify({
                "code":"NO_EMPLOYEES_FOUND",
                "message":"No employees found, please add employee first."
            })
    
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