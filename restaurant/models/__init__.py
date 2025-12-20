import firebase_admin
from firebase_admin import credentials
from flask_sqlalchemy import SQLAlchemy
import pathlib

from restaurant import app
from restaurant.utils import Utils


try:
    db: SQLAlchemy = SQLAlchemy(app=app)
    Utils.logger.info(f"SQLAlchemy: init success!!!")

except Exception as e:
    Utils.logger.critical(f"SQLAlchemy: failed to init db!!\nError:{e} ")
try:
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    KEY_PATH = BASE_DIR / "restaurant-rdb-key.json"

    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(
        cred, {"databaseURL": app.config["FIREBASE_DATABASE_URL"]}
    )

    Utils.logger.info(f"Firebase: init success!!!")

except Exception as e:
    Utils.logger.critical(f"Firebase: failed to init rdb!!\nError:{e} ")