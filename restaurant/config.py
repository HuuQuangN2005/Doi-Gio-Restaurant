import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# ===============================================
# Flask variables
# ===============================================

SECRET_KEY = os.environ.get("SECRET_KEY", "8278baed-7649-45b4-9664-605a21a01233")

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
# RethinkDB variables
# ===============================================

RETHINKDB_HOST = os.environ.get("RETHINKDB_HOST", "localhost")
RETHINKDB_PORT = os.environ.get("RETHINKDB_PORT", "localhost")

