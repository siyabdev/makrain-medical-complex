from database import db
from sqlalchemy.orm import declared_attr

class BaseModel(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()