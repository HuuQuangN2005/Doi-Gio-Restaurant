from flask import Flask

import os
import sys
import logging

import cloudinary


def load_config_from_app(app: Flask):
    print()
    print("=== APP CONFIG ===")
    for key, value in app.config.items():
        print(key, ":", value)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("system.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

from restaurant.utils import Utils

try:
    app = Flask(__name__)

    package_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(package_dir, "config.py")

    app.config.from_pyfile(config_path)


except Exception as e:
    Utils.logger.critical(f"Flask: failed to init app!!\nError:{e} ")
    sys.exit(1)


try:
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_SECRET_KEY"],
    )
    Utils.logger.info(f"Cloudinary: init success!!!")

except Exception as e:
    Utils.logger.critical(f"Cloudinary: failed to init cloudinary!!\nError:{e} ")

app.config["PAGE_SIZE_AT_MAINMENU"] = 5
app.config["PAGE_SIZE_OF_CHOOSE_TABLE"] = 12

app.secret_key = app.config["SECRET_KEY"]