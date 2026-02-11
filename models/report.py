from database import db
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
import enum
from base import BaseModel

#Severity(enum)
class SeverityEnum(enum.Enum):
    normal = "normal"
    mild = "mild"
    moderate = "moderate"
    severe = "severe"
    critical = "critical"
    
#Report
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