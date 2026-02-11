from models.models import GenderEnum, EmployeeRoleEnum

#Create Employee Request
class CreateEmployeeRequest:
    def __init__(self, data):
        self.ward_id = data.get("ward_id")
        self.employee_code = data.get("employee_code")
        self.employee_name = data.get("employee_name")
        self.employee_role = data.get("employee_role")
        self.employee_gender = data.get("employee_gender")
    
    def is_valid(self):

        #Fields required
        if not all([self.ward_id, self.employee_code, self.employee_name, self.employee_role, self.employee_gender]):
            return False, "Missing required fields."
        
        #Validate employee gender against enum
        if self.employee_gender and self.employee_gender not in [employee_gender.value for employee_gender in GenderEnum]:
            return False, "Invalid employee gender provided."
        
        #Validate employee role against enum
        if self.employee_role and self.employee_role not in [employee_role.value for employee_role in EmployeeRoleEnum]:
            return False, "Invalid employee role provided."
        
        return True, None

#Update Employee Request
class UpdateEmployeeRequest:
    def __init__(self, data):
        self.id = data.get("id")
        self.employee_name = data.get("employee_name")
        self.employee_role = data.get("employee_role")
        self.employee_gender = data.get("employee_gender")
    
    def is_valid(self):

        if not self.id:
            return False, "Employee ID missing. Please provide employee ID."
        
        #Validate employee gender against enum
        if self.employee_gender and self.employee_gender not in [employee_gender.value for employee_gender in GenderEnum]:
            return False, "Invalid employee gender provided."
        
        #Validate employee role against enum
        if self.employee_role and self.employee_role not in [employee_role.value for employee_role in EmployeeRoleEnum]:
            return False, "Invalid employee role provided."
        
        return True, None
    
    def has_any_updates(self):
        return any([self.employee_name, self.employee_role, self.employee_gender])
    
#Delete Employee Request
class DeleteEmployeeRequest:
    def __init__(self, data):
        self.id = data.get("id")

    def is_valid(self):

        if not (self.id):
            return False, "Employee ID doesnt exist."
        
        return True, None

#Employee Response
class EmployeeResponse:
    def __init__(self, data):
        self.id = data.id
        self.ward_id = data.ward_id
        self.employee_code = data.employee_code
        self.employee_name = data.employee_name
        self.employee_role = data.employee_role
        self.employee_gender = data.employee_gender
    
    def is_valid(self):

        if not self.id:
            return False, "Employee ID missing. Please provide employee ID."
    
    def to_dict(self):
        return{
            "id": self.id,
            "ward_id": self.ward_id,
            "employee_code": self.employee_code,
            "employee_name": self.employee_name,
            "employee_role": self.employee_role.value if self.employee_role else None,
            "employee_gender": self.employee_gender.value if self.employee_gender else None
        }

#Employee Short Response
class EmployeeShortResponse:
    def __init__(self, data):
        self.id = data.id
        self.employee_name = data.employee_name
        self.employee_role = data.employee_role
        self.employee_gender = data.employee_gender
    
    def to_dict(self):
        return{
            "id": self.id,
            "employee_name": self.employee_name,
            "employee_role": self.employee_role.value if self.employee_role else None,
            "employee_gender": self.employee_gender.value if self.employee_gender else None
        }
    
    @staticmethod
    def from_list(employees):
        return[EmployeeShortResponse(emp).to_dict() for emp in employees]
    
#Employee List Response
class EmployeeListResponse:
    def from_list(employees):
        return [EmployeeResponse(emp).to_dict() for emp in employees]