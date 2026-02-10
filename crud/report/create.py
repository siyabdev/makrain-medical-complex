from flask import current_app
from database import db
from models.models import Report
from sqlalchemy.exc import IntegrityError
from utils.utils import check_enum_format

#Create Report
def create_report_crud(patient_id, employee_id, test_name, result_value, severity, report_date):

    try:
        create_query = Report(
            patient_id = patient_id,
            employee_id = employee_id,
            test_name = test_name,
            result_value = result_value,
            severity = check_enum_format(severity),
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