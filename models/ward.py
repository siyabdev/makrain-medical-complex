from database import db
from sqlalchemy import UniqueConstraint
from base import BaseModel

#Ward
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