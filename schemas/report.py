#Create Report Request
class CreateReportRequest:
    def __init__(self, data):
        self.patient_id = data.get("patient_id")
        self.employee_id = data.get("employee_id")
        self.test_name = data.get("test_name")
        self.result_value = data.get("result_value")
        self.report_date = data.get("report_date")

    def is_valid(self):

        #Fields required
        if not all([self.patient_id, self.employee_id, self.test_name, self.result_value, self.severity, self.report_date]):
            return False, "Missing required fields."
        
        return True, None

#Update Report Request
class UpdateReportRequest:
    def __init__(self, data):
        self.id = data.get("id")
        self.test_name = data.get("test_name")
        self.result_value = data.get("result_value")
        self.report_date = data.get("report_date")
    
    def is_valid(self):

        if not self.id:
            return False, "Report ID missing. Please provide report ID."
            
        return True, None
    
    def has_any_updates(self):
        return any([self.test_name, self.result_value, self.severity, self.report_date])
    
#Delete Report Request
class DeleteReportRequest:
    def __init__(self, data):
        self.id = data.get("id")

    def is_valid(self):

        if not (self.id):
            return False, "Report ID doesnt exist."
        
        return True, None

#Report Response
class ReportResponse:
    def __init__(self, data):
        self.id = data.id
        self.patient_id = data.patient_id
        self.employee_id = data.employee_id
        self.test_name = data.test_name
        self.result_value = data.result_value
        self.severity = data.severity
        self.report_date = data.report_date

        #Loading employee relationship
        if getattr(data, 'employee') and data.employee:
            self.employee_name = data.employee.employee_name
            self.employee_role = data.employee.employee_role if data.employee.employee_role else None
            self.employee_gender = data.employee.employee_gender if data.employee.employee_gender else None
        else:
            self.employee_name = None
            self.employee_role = None
            self.employee_gender = None
        
        #Loading patient relationship
        if getattr(data, "patient") and data.patient:
            self.patient_name = data.patient.patient_name
            self.patient_gender = data.patient.patient_gender if data.patient.patient_gender else None
            self.patient_age = data.patient.patient_age
        else:
            self.patient_name = None
            self.patient_gender = None
            self.patient_age = None

    def is_valid(self):

        if not self.id:
            return False, "Report ID missing. Please provide report ID."
    
    def to_dict(self):
        return{
            "id": self.id,
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "patient_gender": self.patient_gender.value,
            "patient_age": self.patient_age, 
            "employee_id": self.employee_id,
            "employee_name": self.employee_name,
            "employee_role": self.employee_role.value,
            "employee_gender": self.employee_gender.value,
            "test_name": self.test_name,
            "result_value": self.result_value,
            "severity": self.severity.value,
            "report_date": self.report_date.isoformat()
        }

#Report Short Response
class ReportShortResponse:
    def __init__(self, data):
        self.id = data.id
        self.test_name = data.test_name
        self.severity = data.severity
        self.report_date = data.report_date
    
    def to_dict(self):
        return{
            "id": self.id,
            "test_name": self.test_name,
            "severity": self.severity.value,
            "report_date": self.report_date.isoformat()
        }
    
    @staticmethod
    def from_list(reports):
        return[ReportShortResponse(rep).to_dict() for rep in reports]

#Report List Response
class ReportListResponse:
    def from_list(reports):
        return[ReportResponse(rep).to_dict() for rep in reports]
