from flask import Blueprint, request, jsonify, current_app
from crud.employee import create_employee_crud, delete_employee_crud, get_employee_crud, get_employees_crud, get_employees_short_crud, update_employee_crud
from utils.utils import verify_employee, get_employee
from sqlalchemy.exc import IntegrityError
from schemas.employee import CreateEmployeeRequest, DeleteEmployeeRequest, EmployeeResponse, EmployeeListResponse, EmployeeShortResponse, UpdateEmployeeRequest
from auth import require_auth

#Blueprint
employee_bp = Blueprint("employee_bp", __name__ , url_prefix="/employee")

#Create Employee
@employee_bp.route("/create", methods=["POST"])
@require_auth
def create_employee_controller():
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
    
#Delete Employee
@employee_bp.route("/delete", methods=["DELETE"])
@require_auth
def delete_employee_controller():
    data = DeleteEmployeeRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    employee = get_employee(data.id)

    if not employee:
        current_app.logger.info(f"Employee ID '{employee}' doesnt exist.")
        return jsonify({
            "code": "EMPLOYEE_DOESNT_EXIST",
            "message": f"Employee ID '{employee}' doesnt exist, please enter a valid employee ID."
        })
    
    try:
        delete_query = delete_employee_crud(id=data.id)
        if delete_query:
            current_app.logger.info(f"Employee ID {data.id} is deleted.")
            return jsonify({
                "code": "EMPLOYEE_DELETED",
                "message": f"Employee ID {data.id} is deleted."
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

#Get Employee
@employee_bp.route("/get", methods=["GET"])
@require_auth
def get_employee_controller():
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
@employee_bp.route("/all", methods=["GET"])
@require_auth
def get_employees_controller():

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
@employee_bp.route("/short", methods=["GET"])
@require_auth
def get_employees_short_controller():

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

#Update Employee
@employee_bp.route("/update", methods=["PUT"])
@require_auth
def update_employee_controller():
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