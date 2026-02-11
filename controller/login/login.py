from flask import Blueprint, request, jsonify, current_app
from crud.login.login import validate_login_crud
from schemas.login import LoginRequest, LoginResponse
from auth import generate_token
from sqlalchemy.exc import IntegrityError

login_bp = Blueprint("login_bp", __name__ , url_prefix="/employee")

#Login
@login_bp.route("/login", methods=["POST"])
def login():
    data = LoginRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Login schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Login schema error occured {message}."
        }), 400
    
    login = validate_login_crud(username=data.username, password=data.password)

    if not login:
        current_app.logger.error(f"Login failed for username '{data.username}' and password '{data.password}'.")
        return jsonify({
            "code": "LOGIN_FAILED",
            "message": f"Invalid username '{data.username}' or password '{data.password}' provided."
        }), 401
    
    try:
        token = generate_token(login.employee_id, login.username)
        
        response = LoginResponse(token, login.employee_id, login.username, login.is_active)

        current_app.logger.info(f"Login successful for username '{data.username}'.")
        return jsonify({
            "code": "LOGIN_SUCCESS",
            "message": f"Login successful for username '{data.username}'.",
            "data": response.to_dict()
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