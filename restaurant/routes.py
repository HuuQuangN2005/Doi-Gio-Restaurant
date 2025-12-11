from restaurant import app
from restaurant.controllers.page import *

app.add_url_rule('/', 'landing', landing)