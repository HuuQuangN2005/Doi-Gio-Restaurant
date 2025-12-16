from typing import List, Union
from sqlalchemy import or_

from restaurant.database.sql.models.product import Food, Tag, Category
from restaurant.controllers.base import BaseController
from restaurant.database.sql import sql_db as db


class FoodController(BaseController):

    model = Food

    def __init__(self):
        super().__init__(model=self.model)

    def find_by_uuid(self, uuid: str) -> Union[Food, None]:

        results = self.find_by_filters(uuid=uuid)
        return results[0] if results else None

    def find_by_tag(self, tag_names: Union[str, List[str]]) -> List[Food]:

        if isinstance(tag_names, str):
            tag_names = [tag_names]

        return (
            db.session.execute(
                db.select(self.model)
                .join(self.model.tags)
                .where(Tag.name.in_(tag_names))
                .distinct()
            )
            .scalars()
            .all()
        )

    def search_by_keyword(self, keyword: str) -> List[Food]:

        search_term = f"%{keyword.lower()}%"
        return (
            db.session.execute(
                db.select(self.model).where(
                    or_(
                        self.model.name.ilike(search_term),
                        self.model.description.ilike(search_term),
                    )
                )
            )
            .scalars()
            .all()
        )

    def find_by_category_id(self, category_id: int) -> List[Food]:
        
        return self.find_by_filters(category_id=category_id)


class TagController(BaseController):

    model = Tag

    def __init__(self):
        super().__init__(model=self.model)

    def find_by_name(self, name: str) -> Union[Tag, None]:
        results = self.find_by_filters(name=name)
        return results[0] if results else None


class CategoryController(BaseController):

    model = Category

    def __init__(self):
        super().__init__(model=self.model)

    def find_by_name(self, name: str) -> Union[Category, None]:
        results = self.find_by_filters(name=name)
        return results[0] if results else None

    def get_foods_in_category(self, category_id: int) -> List[Food]:
        category = self.find_by_key(category_id)
        if category:
            return category.foods
        return []
