from flask import Flask
from app.config import configs

app = Flask(__name__)
app.config.from_object(configs["development"])

def creat_app():
    from app.web import webIndex
    app.register_blueprint(webIndex)
