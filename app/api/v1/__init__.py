from flask import Blueprint
from app.api.v1.user import bp as user_bp

bp = Blueprint("api/v1", __name__)
bp.register_blueprint(user_bp, url_prefix="/user")
