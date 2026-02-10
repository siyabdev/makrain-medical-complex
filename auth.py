from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "makrainmedicalcomplex"

#Generate token
def generate_token(employee_id, username):
    expiration = datetime.utcnow() + timedelta(hours=24)
    
    payload = {
        "employee_id" : employee_id,
        "username" : username,
        "exp" : expiration
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

#Verify token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        current_app.logger.error(f"Expired signature error {jwt.ExpiredSignatureError}.")
        return None
    except jwt.InvalidTokenError:
        current_app.logger.error(f"Invalid token error {jwt.InvalidTokenError}.")
        return None

#Authentication
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            current_app.logger.info("No token provided.")
            return jsonify({
                "code" : "NO_TOKEN",
                "message" : "No token provided. Please login first."
            }), 401
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            current_app.logger.error(f"Index error {IndexError}.")
            return jsonify({
                "code": "INVALID_TOKEN_FORMAT",
                "message": "Token format is invalid. Use Bearer <token>"
            }), 401
        
        payload = verify_token(token)
        
        if payload is None:
            current_app.logger.error(f"Invalid token {token} provided.")
            return jsonify({
                "code": "INVALID_TOKEN",
                "message": f"Token {token} is invalid or expired. Please login again."
            }), 401
        
        request.employee_id = payload["employee_id"]
        request.username = payload["username"]
        
        return f(*args, **kwargs)
    
    return decorated_function