from restaurant.controllers.user import UserController
from restaurant import app
from flask_login import LoginManager

user_controller = UserController()

login = LoginManager(app)


@login.user_loader
def load_user(id):
    return user_controller.find_by_id(id=id)
