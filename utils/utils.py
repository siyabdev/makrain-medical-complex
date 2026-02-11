from models.models import Employee, Patient, Report, Ward, SeverityEnum

#Checking Enum Format 
def check_enum_format(value):
    return value.lower()

#Get Employee
def get_employee(id):
    employee = Employee.query.filter_by(id=id).first()
    return employee

#Verify Employee
def verify_employee(employee_code, employee_name):
    employee = Employee.query.filter_by(employee_code=employee_code, employee_name=employee_name).first()
    return employee

#Get Patient
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    return patient

#Verify Patient
def verify_patient(patient_code, patient_name):
    patient = Patient.query.filter_by(patient_code=patient_code, patient_name=patient_name).first()
    return patient

#Get Report
def get_report(id):
    report = Report.query.filter_by(id=id).first()
    return report

#Verify Report
def verify_report(patient_id, employee_id, test_name):
    report = Report.query.filter_by(patient_id=patient_id, employee_id=employee_id, test_name=test_name).first()
    return report

#Get Ward
def get_ward(id):
    ward = Ward.query.filter_by(id=id).first()
    return ward

#Verify Ward
def verify_ward(ward_name, floor_number):
    ward = Ward.query.filter_by(ward_name=ward_name, floor_number=floor_number).first()
    return ward

#Calculate Severity Levels
def calculate_severity(result_value):
    if result_value and result_value <= 20:
        return SeverityEnum.normal
    elif result_value and result_value <= 40:
        return SeverityEnum.mild
    elif result_value and result_value <= 60:
        return SeverityEnum.moderate
    elif result_value and result_value <= 80:
        return SeverityEnum.severe
    else:
        return SeverityEnum.critical