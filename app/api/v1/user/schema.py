from operator import and_, or_
from flask import jsonify
from app.extensions import ma
import marshmallow
from .models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class UserRegisterFormSchema(ma.Schema):
    username = marshmallow.fields.String(required=True)


class UserRegisterFileSchema(ma.Schema):
    public_key = marshmallow.fields.Raw(type="file", required=True)


class UserSearchSchema(ma.Schema):
    username = marshmallow.fields.String(required=True)


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
user_register_form_schema = UserRegisterFormSchema()
user_register_file_schema = UserRegisterFileSchema()
user_search_schema = UserSearchSchema()
