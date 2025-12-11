from sqlalchemy import Column, String, Enum
from sqlalchemy.exc import IntegrityError
from enum import Enum as PyEnum

from restaurant import app
from restaurant.database.sql import sql_db
from restaurant.database.sql.models.base import BaseModel, UUIDBaseModel

from flask_login import UserMixin
import hashlib

from colorama import Fore, init

init(autoreset=True) 

class UserRole(PyEnum):
    ADMIN = 1
    COOKER = 2
    CASHIER = 3
    MANAGER = 4
    WAITER = 5


class TableStatus(PyEnum):
    AVAILABLE = 1
    IN_USE = 2
    DIRTY = 3


class User(UUIDBaseModel, UserMixin):
    __tablename__ = "user"

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(200))  # sẽ chuyển vê cloudinary sau khi xong
    user_role = Column(Enum(UserRole), default=UserRole.WAITER)

    def __str__(self):
        return self.name


class Table(BaseModel):
    name = Column(String(50), nullable=False)
    status = Column(Enum(TableStatus), default=TableStatus.AVAILABLE)


def create_default_admin():
    with app.app_context():
        admin = User.query.filter_by(username="admin").first()

        if not admin:
            admin = User(
                name="Administrator",
                username="admin",
                password=hashlib.md5("admin123".encode("utf-8")).hexdigest(),
                user_role=UserRole.ADMIN,
            )

        sql_db.session.add(admin)

        try:
            sql_db.session.commit()
            print(Fore.GREEN + "Default admin created.")
            
        except IntegrityError:
            sql_db.session.rollback()


if __name__ == "__main__":
    with app.app_context():
        sql_db.create_all()
        create_default_admin()