import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# ===============================================
# Flask variables
# ===============================================

SECRET_KEY = os.environ.get("SECRET_KEY", "your_key")

# ===============================================
# MySQL variables
# ===============================================

MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD", "root")
MYSQL_DB = os.environ.get("MYSQL_DATABASE", "restaurant_db")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

SQLALCHEMY_TRACK_MODIFICATIONS = False

# ===============================================
# Fire DB variables
# ===============================================
FIREBASE_DATABASE_URL = os.environ.get('FIREBASE_DATABASE_URL',"your_url")


# ===============================================
# Cloudinary variables
# ===============================================
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME',"your_name")
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY',"your_key")
CLOUDINARY_SECRET_KEY = os.environ.get('CLOUDINARY_SECRET_KEY',"your_key")