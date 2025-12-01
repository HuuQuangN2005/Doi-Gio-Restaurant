from restaurant import app
from restaurant.controllers import page_controller

app.add_url_rule('/', 'landing', page_controller.landing)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)