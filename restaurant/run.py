from restaurant import app
from restaurant.routes import *


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
