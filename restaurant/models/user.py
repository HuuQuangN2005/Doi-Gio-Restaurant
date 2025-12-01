from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Boolean
from enum import Enum as PyEnum

from restaurant import app
from restaurant.models import db

from flask_login import UserMixin
from uuid import uuid4

from restaurant.models.base import BaseModel


class UserRole(PyEnum):
    ADMIN = 1
    DAU_BEP = 2
    THU_NGAN = 3
    QUAN_LY = 4
    PHUC_VU = 5


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))  # sẽ chuyển vê cloudinary sau khi xong
    user_role = Column(Enum(UserRole), default=UserRole.PHUC_VU)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
