from flask import Flask

from .configs import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}?charset=utf8mb4"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


app.config["PAGE_SIZE_OF_CHOOSE_TABLE"] = 10
app.config["NUMBER_OF_TABLE"] = 100

