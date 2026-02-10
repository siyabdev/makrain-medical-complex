from flask import Blueprint, request, jsonify, current_app
from crud.report.delete import delete_report_crud
from utils.utils import get_report
from sqlalchemy.exc import IntegrityError
from schemas.report import DeleteReportRequest
from auth import require_auth

report_delete_bp = Blueprint("report_delete_bp", __name__ , url_prefix="/report")

#Delete Report
@report_delete_bp.route("delete", methods=["DELETE"])
@require_auth
def delete_report():
    data = DeleteReportRequest(request.json)
    valid, message = data.is_valid()

    if not valid:
        current_app.logger.error(f"Schema error {message}.")
        return jsonify({
            "code": "SCHEMA_ERROR",
            "message": f"Schema error occured {message}."
        }), 400
    
    report = get_report(data.id)

    if not report:
        current_app.logger.info(f"Report ID '{report}' doesnt exist.")
        return jsonify({
            "code": "REPORT_DOESNT_EXIST",
            "message": f"Report ID '{report}' doesnt exist, please enter a valid report ID."
        })
    
    try:
        delete_query = delete_report_crud(id=data.id)
        if delete_query:
            current_app.logger.info(f"Report ID {data.id} is deleted.")
            return jsonify({
                "code": "REPORT_DELETED",
                "message": f"Report ID {data.id} is deleted."
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