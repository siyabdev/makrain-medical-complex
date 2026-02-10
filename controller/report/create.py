from flask import Blueprint, request, jsonify, current_app
from crud.report.create import create_report_crud
from utils.utils import verify_report, calculate_severity
from sqlalchemy.exc import IntegrityError
from schemas.report import CreateReportRequest, ReportResponse
from auth import require_auth

report_create_bp = Blueprint("report_create_bp", __name__ , url_prefix="/report")

#Create Report
@report_create_bp.route("/create", methods=["POST"])
@require_auth
def create_report():
    data = CreateReportRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    report = verify_report(data.patient_id, data.employee_id, data.test_name)

    if report:
        current_app.logger.info(f"Report already exists '{report}'.")
        return jsonify({
            "code": "REPORT_ALREADY_EXISTS",
            "message": f"This report '{report}' already exists, try a new one."
        }), 403
    
    #Calculation
    severity = calculate_severity(data.result_value)

    try:
        new_report = create_report_crud(
            patient_id = data.patient_id,
            employee_id = data.employee_id,
            test_name = data.test_name,
            result_value = data.result_value,
            severity = severity,
            report_date = data.report_date
        )

        current_app.logger.info(f"Report {new_report} created.")
        return jsonify({
            "code": "REPORT_CREATED",
            "data": ReportResponse(new_report).to_dict()
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