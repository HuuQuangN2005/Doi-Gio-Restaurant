import json
import os
from restaurant.utils import Utils
from restaurant import app
from restaurant.services import *
from restaurant.models import db
from restaurant.models.sql import Category, Food,Table

def load_user(filename="user.json"):

    with app.app_context():
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, filename)

            if not os.path.exists(file_path):
                Utils.logger.error(f"Data: {file_path} not exists!!")
                return False

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                users_list = data.get("users", [])

            success_count = 0
            for user_data in users_list:
                if user_service.create(user_data):
                    success_count += 1
            
            Utils.logger.info(f"Data: Success add users!!")
            return True

        except Exception as e:
            Utils.logger.critical(f"Data: {str(e)}")
            return False

def load_data_with_no_img(model_class,filename="user.json"):

    with app.app_context():
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, filename)

            if not os.path.exists(file_path):
                Utils.logger.error(f"Data: {file_path} not exists!!")
                return False

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                model_columns = model_class.__table__.columns.keys()

                for item in data:
                    filtered_item = {k: v for k, v in item.items() if k in model_columns}
                    
                    obj = model_class(**filtered_item)
                    db.session.add(obj)
                
                db.session.commit()
                Utils.logger.info(f"Data: Success add data to {model_class.__tablename__}!!")

        except Exception as e:
            Utils.logger.critical(f"Data: {str(e)}")
            return False
        
        
if __name__ == "__main__":
    load_user()
    
    load_data_with_no_img(Category, "category.json")
    load_data_with_no_img(Food, "food.json")
    load_data_with_no_img(Table, "table.json")