from restaurant import app
from flask_sqlalchemy import SQLAlchemy

sql_db:SQLAlchemy = SQLAlchemy(app = app)
