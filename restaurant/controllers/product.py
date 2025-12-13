from restaurant.database.sql.models.product import Food


class ProductController:
    def __init__(self):
        pass

    def find_by_id(self, id:int):
        return Food.query.get(int(id))
        
    def find_by_uuid(self,uuid:str):
        return Food.query.get(str(uuid))

    def find_by_tag(self):
        pass