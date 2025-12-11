from flask import Flask
import os
import sys

def create_app(config:str = 'config.py') -> Flask:
    try:
        app = Flask(__name__)
        
        package_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(package_dir, config)

        app.config.from_pyfile(config_path)
               
        return app
    
    except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
def load_config_from_app(app:Flask):
    print()
    print("=== APP CONFIG ===")
    for key, value in app.config.items():
        print(key, ":", value)


    
app = create_app()

#load_config_from_app(app=app)