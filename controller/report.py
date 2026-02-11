from flask import Blueprint, request, jsonify, current_app
from crud.report import create_report_crud, delete_report_crud, get_report_crud, get_reports_crud, get_reports_short_crud, update_report_crud
from utils.utils import verify_report, calculate_severity, get_report
from sqlalchemy.exc import IntegrityError
from schemas.report import CreateReportRequest, DeleteReportRequest, ReportResponse, ReportListResponse, ReportShortResponse, UpdateReportRequest
from auth import require_auth

#Blueprint
report_bp = Blueprint("report_bp", __name__ , url_prefix="/report")

#Create Report
@report_bp.route("/create", methods=["POST"])
@require_auth
def create_report_controller():
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

#Delete Report
@report_bp.route("delete", methods=["DELETE"])
@require_auth
def delete_report_controller():
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

#Get Report
@report_bp.route("/get", methods=["GET"])
@require_auth
def get_report_controller():
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
@report_bp.route("/all", methods=["GET"])
@require_auth
def get_reports_controller():

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
@report_bp.route("/short", methods=["GET"])
@require_auth
def get_reports_short_controller():

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

#Update Report
@report_bp.route("/update", methods=["PUT"])
@require_auth
def update_report_controller():
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