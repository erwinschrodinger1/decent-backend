from flask import Blueprint

bp = Blueprint("user", __name__)

from app.api.v1.user import routes
