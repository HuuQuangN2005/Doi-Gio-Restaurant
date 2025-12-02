from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Text, Enum
from enum import Enum as PyEnum

from restaurant.models.base import UUIDBaseModel
from restaurant import app
from restaurant.models import db

from restaurant.models.user import User, Table
from restaurant.models.product import Food


class ReceiptStatus(PyEnum):
    OPEN = 1
    CLOSED = 2
    PAID = 3

class ReceiptItemStatus(PyEnum):
    PENDING = 1        
    COOKING = 2        
    DONE = 3
    CANCELLED = 4   

class Receipt(UUIDBaseModel):
    __tablename__ = "receipt"

    order_by = Column(Integer, ForeignKey(Table.id), nullable=False)
    created_by = Column(Integer, ForeignKey(User.id), nullable=False)
    status = Column(Enum(ReceiptStatus), default=ReceiptStatus.CLOSED)
    details = relationship("ReceiptItems", backref="receipt", lazy=True)


class ReceiptItems(db.Model):
    __tablename__ = "receipt_items"

    id = Column(Integer, autoincrement=True, primary_key=True)
    quantity = Column(Integer, default=0)
    note = Column(Text)
    status = Column(Enum(ReceiptItemStatus),default=ReceiptItemStatus.PENDING)
    food_id = Column(Integer, ForeignKey(Food.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
