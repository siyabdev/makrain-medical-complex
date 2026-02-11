from flask import current_app
from database import db
from models.report import Report
from sqlalchemy.exc import IntegrityError
from utils.utils import get_report, calculate_severity

#Create Report
def create_report_crud(patient_id, employee_id, test_name, result_value, severity, report_date):

    try:
        create_query = Report(
            patient_id = patient_id,
            employee_id = employee_id,
            test_name = test_name,
            result_value = result_value,
            severity = severity,
            report_date = report_date
        )

        db.session.add(create_query)
        db.session.commit()

        return create_query
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Delete Report
def delete_report_crud(id):
    try:
        delete_query = Report.query.filter_by(id=id).first()
        db.session.delete(delete_query)
        db.session.commit()

        return delete_query
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get Report
def get_report_crud(id):
    try:
        report = get_report(id)
        return report
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Get Reports
def get_reports_crud():
    try:
        reports = Report.query.all()
        db.session.commit()
        return reports
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e
    
#Get Short Details (Reports)
def get_reports_short_crud():
    try:
        reports = Report.query.with_entities(Report.id, Report.test_name, Report.severity, Report.report_date).all()
        db.session.commit()
        return reports
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e

#Update Report
def update_report_crud(id, test_name, result_value, report_date):
    report = get_report(id)

    if not report:
        return report == False
    try:
        #Update provided fields
        if test_name:
            report.test_name = test_name
        
        if result_value:
            report.result_value = result_value
        
        if report_date:
            report.report_date = report_date

        #Calculate Severity Levels
        report.severity = calculate_severity(
            report.result_value
        )
        
        db.session.commit()
        return report
    
    except IntegrityError as error:
        current_app.logger.error(f"Integrity error {error}.")
        raise error
    
    except Exception as e:
        current_app.logger.error(f"Exceptional error {e}.")
        raise e