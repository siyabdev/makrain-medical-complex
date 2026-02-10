from flask import Blueprint, request, jsonify, current_app
from crud.report.update import update_report_crud
from utils.utils import get_report
from sqlalchemy.exc import IntegrityError
from schemas.report import UpdateReportRequest, ReportResponse
from auth import require_auth

report_update_bp = Blueprint("report_update_bp", __name__ , url_prefix=("/report"))

#Update Report
@report_update_bp.route("/update", methods=["PUT"])
@require_auth
def update_report():
    data = UpdateReportRequest(request.json)
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
    
    report = get_report(data.id)

    if not report:
        current_app.logger.error(f"Report ID '{report}' not found.")
        return jsonify({
            "code": "REPORT_NOT_FOUND", 
            "message": f"Report ID '{report}' not found."
        }), 404
    
    try:
        updated_report = update_report_crud(id=data.id, test_name = data.test_name, result_value = data.result_value, report_date = data.report_date)
        current_app.logger.info(f"Report updated {updated_report}.")
        return jsonify({
            "code": "REPORT_UPDATED",
            "data": ReportResponse(updated_report).to_dict()
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