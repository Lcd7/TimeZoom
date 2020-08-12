from flask import Flask
from app.config import configs

def creat_app():
    app = Flask(__name__)
    app.config.from_object(configs["development"])
    register_blueprints(app)
    return app

def register_blueprints(app):
    from app.web import blue_index
    app.register_blueprint(blue_index)