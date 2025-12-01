from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text

from restaurant.models.base import BaseModel, UUIDBaseModel
from restaurant import app
from restaurant.models import db

class Category(BaseModel):
    __tablename__ = "category"

    name = Column(String(50), nullable=False, unique=True)
    foods = relationship("Food", backref="category", lazy=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name

class Food(UUIDBaseModel):
    __tablename__ = "food"

    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship(
        "Tag",
        secondary="food_tag",
        lazy="subquery",
        backref=backref("foods", lazy=True),
    )
    
    def __str__(self):
        return self.name

food_tag = db.Table(
    "food_tag",
    Column("food_id", Integer, ForeignKey("food.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key=True),
)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()