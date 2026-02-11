from models.patient import GenderEnum

#Create Patient Request
class CreatePatientRequest:
    def __init__(self, data):
        self.ward_id = data.get("ward_id")
        self.patient_code = data.get("patient_code")
        self.patient_name = data.get("patient_name")
        self.patient_gender = data.get("patient_gender")
        self.patient_age = data.get("patient_age")
    
    def is_valid(self):

        #Fields required
        if not self.ward_id:
            return False, "Missing ward ID. Please provide ward ID."

        if not self.patient_code:
            return False, "Missing patient code. Please provide patient code."

        if not self.patient_name:
            return False, "Missing patient name. Please provide patient name."

        if not self.patient_gender:
            return False, "Missing patient gender. Please provide patient gender."

        if not self.patient_age:
            return False, "Missing patient age. Please provide patient age."

        #Validate patient age value
        if self.patient_age and self.patient_age < 0:
            return False, "Patient age should be greater than or equal to 0."
        
        #Validate patient gender against enum
        if self.patient_gender and self.patient_gender not in [patient_gender.value for patient_gender in GenderEnum]:
            return False, "Invalid patient gender provided."
        
        return True, None
    
#Update Patient Request
class UpdatePatientRequest:
    def __init__(self, data):
        self.id = data.get("id")
        self.patient_name = data.get("patient_name")
        self.patient_gender = data.get("patient_gender")
        self.patient_age = data.get("patient_age")
    
    def is_valid(self):

        if not self.id:
            return False, "Patient ID missing. Please provide patient ID."
        
        #Validate patient age value
        if self.patient_age and self.patient_age < 0:
            return False, "Patient age should be greater than or equal to 0."
        
        #Validate patient gender against enum
        if self.patient_gender and self.patient_gender not in [patient_gender.value for patient_gender in GenderEnum]:
            return False, "Invalid patient gender provided."
        
        return True, None
    
    def has_any_updates(self):
        return any([self.patient_name, self.patient_gender, self.patient_age])

#Delete Patient Request
class DeletePatientRequest:
    def __init__(self, data):
        self.id = data.get("id")

    def is_valid(self):

        if not (self.id):
            return False, "Patient ID doesnt exist."
        
        return True, None
    
#Patient Response
class PatientResponse:
    def __init__(self, data):
        self.id = data.id
        self.ward_id = data.ward_id
        self.patient_code = data.patient_code
        self.patient_name = data.patient_name
        self.patient_gender = data.patient_gender
        self.patient_age = data.patient_age

    def is_valid(self):

        if not self.id:
            return False, "Patient ID missing. Please provide patient ID."
    
    def to_dict(self):
        return{
            "id": self.id,
            "ward_id": self.ward_id,
            "patient_code": self.patient_code,
            "patient_name": self.patient_name,
            "patient_gender": self.patient_gender.value if self.patient_gender else None,
            "patient_age":self.patient_age
        }

#Patient Short Response
class PatientShortResponse:
    def __init__(self, data):
        self.id = data.id
        self.patient_name = data.patient_name
        self.patient_gender = data.patient_gender
        self.patient_age = data.patient_age

    def to_dict(self):
        return{
            "id": self.id,
            "patient_name": self.patient_name,
            "patient_gender": self.patient_gender.value if self.patient_gender else None,
            "patient_age":self.patient_age
        }
    
    @staticmethod
    def from_list(patients):
        return[PatientShortResponse(pat).to_dict() for pat in patients]

#Patient List Response
class PatientListResponse:
    def from_list(patients):
        return[PatientResponse(pat).to_dict() for pat in patients]