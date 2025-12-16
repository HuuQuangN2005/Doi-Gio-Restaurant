from restaurant import app
from flask_login import LoginManager
from restaurant.controllers import *
login = LoginManager(app)


@login.user_loader
def load_user(id):
    return user_controller.find_by_key(id)
