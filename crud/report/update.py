from flask import current_app
from database import db
from utils.utils import get_report, calculate_severity
from sqlalchemy.exc import IntegrityError

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