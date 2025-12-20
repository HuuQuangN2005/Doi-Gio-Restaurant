from restaurant.models.sql import Food, Category


class ProductService:
    def __init__(self):
        pass

    def get_foods(self) -> list[Food]:
        return Food.query.filter(Food.active == True).all()

    def get_all_categories(self) -> list[Category]:
        return Category.query.filter(Category.active == True).all()

    def get_food_by_category(self, category_id: int = None) -> list[Food]:
        food = Food.query.filter(Food.active == True)

        if category_id:
            food = food.filter_by(Food.category_id == category_id)

        return food.all()

    def get_food_by_id(self, food_id: int) -> Food:
        food = Food.query.filter(Food.active == True)
        return food.query.filter(Food.id == food_id).first()

    def get_food_by_name(self, name: str) -> list[Food]:
        food = Food.query.filter(Food.active == True)

        if name:
            food = food.filter(Food.name.ilike(f"%{name}%"))

        return food.all()


product_service = ProductService()
