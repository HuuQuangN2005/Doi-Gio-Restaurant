from flask import Flask
from flask_login import LoginManager

import sys
import cloudinary

from restaurant.controllers import *
from restaurant import app


login = LoginManager(app)


@login.user_loader
def load_user(id):
    return user_controller.find_by_key(id)


try:
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_SECRET_KEY"],
    )
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
