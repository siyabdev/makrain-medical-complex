from database import db
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
import enum
from base import BaseModel

#Gender(enum)
class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

#Employee role(enum)
class EmployeeRoleEnum(enum.Enum):
    doctor = "doctor"
    staff = "staff"

#Severity(enum)
class SeverityEnum(enum.Enum):
    normal = "normal"
    mild = "mild"
    moderate = "moderate"
    severe = "severe"
    critical = "critical"

#Login class
class Login(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    __table_args__ = (
    UniqueConstraint("username", name="unique_employee_username"),
    UniqueConstraint("employee_id", name="unique_employee_id"),
    CheckConstraint("length(username) > 6", name="check_username_min_length"),
    CheckConstraint("length(password) > 8", name="check_password_min_length"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "username": self.username,
            "password": self.password,
            "is_active": self.is_active
    }

    @classmethod
    def to_dict_list(cls, logins):
        return [log.to_dict() for log in logins]

#Employee class
class Employee(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, db.ForeignKey('ward.id', ondelete='SET NULL'), nullable=False)
    employee_code = db.Column(db.String(120), nullable=False)
    employee_name = db.Column(db.String(120), nullable=False)
    employee_role = db.Column(db.Enum(EmployeeRoleEnum, name="employee_role_enum"), nullable=False)
    employee_gender = db.Column(db.Enum(GenderEnum, name="employee_gender_enum"), nullable=False)

    __table_args__ = (
    UniqueConstraint("employee_code", name="unique_employee_code"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "ward_id": self.ward_id,
            "employee_code": self.employee_code,
            "employee_name": self.employee_name,
            "employee_role": self.employee_role.value,
            "employee_gender": self.employee_gender.value
    }

    @classmethod
    def to_dict_list(cls, employees):
        return [emp.to_dict() for emp in employees]

#Ward class
class Ward(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    ward_name = db.Column(db.String(120), nullable=False)
    floor_number = db.Column(db.Integer, nullable=False)

    __table_args__ = (
    UniqueConstraint("ward_name", name="unique_ward_name"),
    )

    def to_dict(self):
        return{
            "id": self.id,
            "ward_name": self.ward_name,
            "floor_number": self.floor_number
    }

    @classmethod
    def to_dict_list(cls, wards):
        return [war.to_dict() for war in wards]

#Patient class
class Patient(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, db.ForeignKey('ward.id', ondelete='CASCADE'), nullable=False)
    patient_code = db.Column(db.String(120), nullable=False)
    patient_name = db.Column(db.String(120), nullable=False)
    patient_gender = db.Column(db.Enum(GenderEnum, name="patient_gender_enum"), nullable=False)
    patient_age = db.Column(db.Integer, nullable=False)

    __table_args__ = (
    UniqueConstraint("patient_code", name="unique_patient_code"),
    CheckConstraint("patient_age >= 0", name="min_patient_age_check"),
    )

    def to_dict(self):
        return{
            "id": self.id,
            "ward_id": self.ward_id,
            "patient_code": self.patient_code,
            "patient_name": self.patient_name,
            "patient_gender": self.patient_gender.value,
            "patient_age": self.patient_age
    }

    @classmethod
    def to_dict_list(cls, patients):
        return [pat.to_dict() for pat in patients]
    
#Report class
class Report(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    test_name = db.Column(db.String(120), nullable=False)
    result_value = db.Column(db.Float, nullable=False)
    severity = db.Column(db.Enum(SeverityEnum, name="severity_enum"))
    report_date = db.Column(db.Date, nullable=False)

    __table_args__ = (
    CheckConstraint("result_value <= 100", name="min_patient_age_check"),
    )

    #Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    patient = relationship("Patient", foreign_keys=[patient_id])

    def to_dict(self):
        return{
            "id": self.id,
            "patient_id": self.patient_id,
            "employee_id": self.employee_id,
            "test_name": self.test_name,
            "result_value": float(self.result_value),
            "severity": self.severity.value,
            "report_date": self.report_date.isoformat()
    }

    @classmethod
    def to_dict_list(cls, reports):
        return [rep.to_dict() for rep in reports]