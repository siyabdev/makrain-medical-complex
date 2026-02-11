from database import db
from sqlalchemy import UniqueConstraint, CheckConstraint
from base import BaseModel

#Login
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