from restaurant.database.sql import sql_db
from sqlalchemy import Column, Integer, DateTime, Boolean, String
from datetime import datetime
from uuid import uuid4


class BaseModel(sql_db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    created_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)


class UUIDBaseModel(sql_db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String(36), default=lambda: str(uuid4()), unique=True)
    created_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)
