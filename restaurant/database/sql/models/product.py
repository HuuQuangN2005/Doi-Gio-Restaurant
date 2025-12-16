from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text

from restaurant.database.sql.models.base import BaseModel, UUIDBaseModel
from restaurant import app
from restaurant.database.sql import sql_db

from colorama import Fore, init

init(autoreset=True)

class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(50), nullable=False, unique=True)
    foods = relationship("Food", backref="category", lazy=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    __tablename__ = "tags"
     
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Food(UUIDBaseModel):
    __tablename__ = "foods"

    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False, default=0)
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship(
        "Tag",
        secondary="foods_tags",
        lazy="subquery",
        backref=backref("foods", lazy=True),
    )

    def __str__(self):
        return self.name


food_tag = sql_db.Table(
    "foods_tags",
    Column("food_id", Integer, ForeignKey("foods.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


if __name__ == "__main__":
    with app.app_context():
        sql_db.create_all()
        print(Fore.GREEN + "Product models created.")