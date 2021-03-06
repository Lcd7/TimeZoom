from flask import Flask
from app.config import configs

def creat_app():
    app = Flask(__name__)
    app.config.from_object(configs["development"])
    register_blueprints(app)
    return app

def register_blueprints(app):
    from app.web import webIndex, webBack
    app.register_blueprint(webIndex)
    app.register_blueprint(webBack)