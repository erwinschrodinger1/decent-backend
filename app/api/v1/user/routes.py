from http.client import BAD_REQUEST
from flask import Response, json, request
from ..user import bp
from .schema import (
    user_schema,
    user_schemas,
    user_register_form_schema,
    user_register_file_schema,
    user_search_schema,
)
from .controllers import register_user, validate_user, get_all_user


@bp.route("/register", methods=["POST"])
def register():
    form_errors = user_register_form_schema.validate(request.form)
    file_errors = user_register_file_schema.validate(request.files)
    errors: dict[str, list[str]] = {}
    if form_errors:
        errors.update(form_errors)
    if file_errors:
        errors.update(file_errors)
    if errors != {}:
        return Response(json.dumps(errors), BAD_REQUEST)

    username = request.form["username"]
    public_key = request.files["public_key"]
    return register_user(username, public_key)


@bp.route("/validate", methods=["GET"])
def getOne():
    errors = user_search_schema.validate(request.args)
    if errors:
        return Response(json.dumps(errors), BAD_REQUEST)

    return validate_user(request.args["username"])


@bp.route("/get", methods=["GET"])
def getAll():
    return get_all_user()
