from flask import Blueprint
blue_index = Blueprint('blue_index', __name__, url_prefix = '/index')

import app.web.index