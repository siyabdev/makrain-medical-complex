from database import db
from sqlalchemy import UniqueConstraint
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

#Employee
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