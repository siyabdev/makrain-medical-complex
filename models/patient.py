from database import db
from sqlalchemy import UniqueConstraint, CheckConstraint
import enum
from base import BaseModel

#Gender(enum)
class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

#Patient
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