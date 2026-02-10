from flask import Blueprint, request, jsonify, current_app
from crud.report.get import get_report_crud, get_reports_crud, get_reports_short_crud
from schemas.report import ReportResponse, ReportListResponse, ReportShortResponse
from sqlalchemy.exc import IntegrityError
from auth import require_auth

report_get_bp = Blueprint("report_get_bp", __name__ , url_prefix="/report")

#Get Report
@report_get_bp.route("/get", methods=["GET"])
@require_auth
def get_report():
    data = request.json
    id = data.get("id")

    if not id:
        current_app.logger.error(f"Wrong report ID {id} provided.")
        return jsonify({
            "code": "WRONG_REPORT_ID_PROVIDED",
            "message": f"Please enter correct report ID."
        }), 403
    
    report = get_report_crud(id=id)

    try:
        if report:
            current_app.logger.info(f"Report '{report}' response returned.")
            return ReportResponse(report).to_dict()
        
        else:
            current_app.logger.error(f"Report ID {id} is not registered.")
            return jsonify({
                "code":"REPORT_ID_DOESNT_EXIST",
                "message": f"Report ID {id} is not registered, please try another."
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

#Get Reports
@report_get_bp.route("/all", methods=["GET"])
@require_auth
def get_reports():

    try:
        reports = get_reports_crud()

        if reports:
            current_app.logger.info(f"Reports '{reports}' response returned.")
            return ReportListResponse.from_list(reports) 
        else:
            current_app.logger.error("No reports found.")
            return jsonify({
                "code":"NO_REPORTS_FOUND",
                "message":"No reports found, please add report first."
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

#Get Short Details (Reports)
@report_get_bp.route("/short", methods=["GET"])
@require_auth
def get_reports_short():

    try:
        reports = get_reports_short_crud()

        if reports:
            current_app.logger.info(f"Reports '{reports}' response returned.")
            return ReportShortResponse.from_list(reports)

        else:
            current_app.logger.error("No reports found")
            return jsonify({
                "code":"NO_REPORTS_FOUND",
                "message":"No reports found, please add report first."
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