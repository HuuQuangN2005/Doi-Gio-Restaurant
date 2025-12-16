import firebase_admin
from firebase_admin import credentials
from restaurant import app
from firebase_admin import db as rdb
import pathlib


try:
    BASE_DIR = pathlib.Path(__file__).resolve().parent
    KEY_PATH = BASE_DIR / "restaurant-rdb-key.json"

    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(
        cred, {"databaseURL": app.config["FIREBASE_DATABASE_URL"]}
    )
except ValueError:
    pass
except Exception as e:
    print(f"Error in init firebase db: {e}")