"""API V1 Blueprint"""
# http://stackoverflow.com/questions/24420857/what-are-flask-blueprints-exactly
from flask import Blueprint


api = Blueprint('api_v1', __name__)

import aflux_assurance_server.api.v1.views