from flask import request, jsonify

from app import db, jwt
from app.routers.auth import bp
from app.models import Users, RevokedTokenModel
from app.schemas import UsersDeserializingSchema
from app.errors.handlers import bad_request, error_response

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

from marshmallow import ValidationError

user_schema = UsersDeserializingSchema()


@bp.post("/register")
def register() -> str:
    """
    Endpoint for adding a new user to the database

    Returns
    -------
    str
        A JSON object containing the success message
    """
    try:
        result = user_schema.load(request.json)

    except ValidationError as e:
        return bad_request(e.messages)

    if Users.query.filter_by(username=result["username"]).first():
        return bad_request("Username already in use")

    if Users.query.filter_by(email=result["email"]).first():
        return bad_request("Email already in use")

    user = Users(
        username=result["username"],
        first_name=result["first_name"],
        last_name=result["last_name"],
        email=result["email"],
        birthday=result["birthday"],
    )

    user.set_password(result["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Successfully registered"}), 201


@bp.post("/login")
def login() -> str:
    """
    Endpoint for authorizing a user and retrieving a JWT

    Returns
    -------
    str
        A JSON object containing both the access JWT and the refresh JWT
    """
    try:
        result = user_schema.load(request.json)

    except ValidationError as e:
        return bad_request(e.messages)

    user = Users.query.filter_by(username=result["username"]).first()

    if user is None or not user.check_password(result["password"]):
        return error_response(401, message="Invalid username or password")

    tokens = {
        "access_token": create_access_token(identity=user.id, fresh=True),
        "refresh_token": create_refresh_token(identity=user.id),
    }

    return jsonify(tokens), 200


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh() -> str:
    """
    Endpoint in order to retrieve a new access JWT using the refresh JWT.
    A non-fresh access token is returned because the password is not involved in this transaction

    Returns
    -------
    str
        A JSON object containing the new access token
    """
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id, fresh=False)
    payload = {"access_token": new_token}

    return jsonify(payload), 200


@bp.post("/fresh-login")
def fresh_login() -> str:
    """
    Endpoint for requesting a new fresh access token

    Returns
    -------
    str
        A JSON object containing
    """
    try:
        result = user_schema.load(request.json)

    except ValidationError as e:
        return bad_request(e.messages)

    user = Users.query.filter_by(username=result["username"]).first()

    if user is None or not user.check_password(result["password"]):
        return error_response(401, message="Invalid username or password")

    new_token = create_access_token(identity=user.id, fresh=True)
    payload = {"access_token": new_token}

    return jsonify(payload), 200
