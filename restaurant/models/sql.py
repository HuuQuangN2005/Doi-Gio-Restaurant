from restaurant.models import db
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    String,
    Enum,
    Text,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship, backref
from enum import Enum as PyEnum

from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4

from restaurant import app

# ----------------------------------------------------------------------------


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


# ----------------------------------------------------------------------------


class UserRole(PyEnum):
    ADMIN = 1
    COOKER = 2
    CASHIER = 3
    MANAGER = 4
    WAITER = 5
    CUSTOMER = 6


class TableStatus(PyEnum):
    AVAILABLE = 1
    IN_USE = 2
    RESERVED = 3


# ----------------------------------------------------------------------------


class User(UUIDBaseModel):
    __tablename__ = "users"

    name = Column(String(50), nullable=False)
    address = Column(String(250))
    gender = Column(Integer, nullable=False, default=0)
    email = Column(String(100), nullable=True)
    phone = Column(String(12), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)

    type = Column(String(50))
    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": type}

    @property
    def is_active(self):
        return self.active == True

    def get_id(self):
        return str(self.uuid)

    orders_as_customer = relationship(
        "Receipt", backref="customer", foreign_keys="[Receipt.customer_id]", lazy=True
    )
    orders_as_employee = relationship(
        "Receipt", backref="employee", foreign_keys="[Receipt.employee_id]", lazy=True
    )


class Employee(User, UserMixin):
    __tablename__ = "employees"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    username = Column(String(50), nullable=False, unique=True)
    password =  Column(String(150), nullable=False)
    avatar = Column(String(200))

    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }


# ----------------------------------------------------------------------------


class Category(UUIDBaseModel):
    __tablename__ = "categories"

    name = Column(String(50), nullable=False, unique=True)
    foods = relationship("Food", backref="category", lazy=True)

    def __str__(self):
        return self.name


class Food(UUIDBaseModel):
    __tablename__ = "foods"

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    name = Column(String(100), nullable=False)
    description = Column(Text(),nullable=True)
    price = Column(Float, nullable=False)
    image = Column(String(200))

    def __str__(self):
        return self.name


# ----------------------------------------------------------------------------


class Table(BaseModel):
    __tablename__ = "tables"
    name = Column(String(50), nullable=False, unique=True)
    status = Column(Enum(TableStatus), default=TableStatus.AVAILABLE)
    capacity = Column(Integer, default=6)

    def __str__(self):
        return self.name

    @property
    def get_status(self):
        return self.status


class Receipt(UUIDBaseModel):
    __tablename__ = "receipts"

    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)

    discount_rate = Column(Float, default=0)
    total_amount = Column(Float, default=0)
    is_paid = Column(Boolean, default=False)

    details = relationship("ReceiptDetail", backref="receipt", lazy=True)

class ReceiptDetail(BaseModel):
    __tablename__ = "receipt_details"

    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)

    quantity = Column(Integer, default=1)
    price = Column(Float)

    note = Column(Text(), nullable=True)
    status = Column(String(50), default="PENDING")


# ----------------------------------------------------------------------------


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        