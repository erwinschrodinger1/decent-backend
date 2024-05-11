import os
from flask import Flask, current_app, send_from_directory
from flask import Blueprint
from config import Config
from app.extensions import db, ma


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="", static_folder="/static/public_keys")
    app.config.from_object(config_class)

    from flask_cors import CORS

    CORS(app)

    # Extensions
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    from app.api.v1 import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.route("/test/")
    def test_page():
        return "<h1>Testing the Flask Application</h1>"

    @app.route("/uploads/<path:filename>", methods=["GET", "POST"])
    def download(filename):
        uploads = os.path.join(
            current_app.root_path, "../", app.config["UPLOAD_FOLDER"]
        )
        return send_from_directory(uploads, filename)

    with app.app_context():
        db.create_all()

    return app
