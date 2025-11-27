from restaurant import app
from flask import render_template
@app.route('/')
def index():
    return render_template('pages/landing/index.html')

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)