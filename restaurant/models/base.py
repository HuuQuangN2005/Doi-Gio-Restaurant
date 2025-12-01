from restaurant.models import db
from sqlalchemy import Column, Integer, DateTime, Boolean, String
from datetime import datetime
from uuid import uuid4


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    created_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)


class UUIDBaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True)
    created_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

