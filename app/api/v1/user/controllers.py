import os
from flask import app, flash, jsonify, redirect, request, url_for
from werkzeug.utils import secure_filename
from config import Config
from .models import User
from app.extensions import db
from .schema import user_schema, user_schemas
import json


def register_user(username, file):
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        user = User(username, filename)
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user)


def validate_user(username):
    user = User.query.filter_by(username=username).first()
    if user == {}:
        return jsonify({"message": "User Not Valid"})
    return user_schema.jsonify(user)


def get_all_user():
    users = User.query.all()
    return user_schemas.jsonify(users)
