from flask import current_app
from database import db
from utils.utils import get_report
from models.models import Report
from sqlalchemy.exc import IntegrityError

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