from datetime import timedelta
from typing import Optional, Tuple

import redis
from flask import current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from marshmallow import ValidationError

from app import db, jwt
from app.errors.handlers import bad_request, error_response
from app.models import Users
from app.routers.auth import bp

ACCESS_EXPIRES = timedelta(hours=1)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

# @bp.post("/register")
# def register():
#     """
#     Endpoint for adding a new user to the database

#     Returns
#     -------
#     str
#         A JSON object containing the success message
#     """
#     try:
#         result = request.json
#     except ValidationError as e:
#         return bad_request(e.messages)

#     if Users.query.filter_by(username=result["username"]).first():
#         return bad_request("Username already in use")

#     if Users.query.filter_by(email=result["email"]).first():
#         return bad_request("Email already in use")

#     user = Users(
#         email=result["email"],
#     )

#     user.set_password(result["password"])

#     db.session.add(user)
#     db.session.commit()

#     return jsonify({"msg": "Successfully registered"}), 201


@bp.route('/login')
def login():
    """
    Endpoint for authorizing a user and retrieving a JWT

    Returns
    -------
    str
        A JSON object containing both the access JWT and the refresh JWT
    """

    auth = request.authorization
    # try:
    #     result = request.json

    # except ValidationError as e:
    #     return bad_request(e.messages)

    # user = Users()
    # if user is None or not user.check_password(result["password"]):
    #     return error_response(401, message="Invalid username or password")
    if auth and (auth.username == current_app.config['USER_NAME'] and auth.password == current_app.config['PASSWORD']):
        tokens = {
            "access_token": create_access_token(identity='id', fresh=True),
            "refresh_token": create_refresh_token(identity='id'),
        }

        return jsonify(tokens), 200

    return error_response(401, message="Invalid username or password")  


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
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
def fresh_login():
    """
    Endpoint for requesting a new fresh access token

    Returns
    -------
    str
        A JSON object containing
    """
    # try:
    #     result = user_schema.load(request.json)

    # except ValidationError as e:
    #     return bad_request(e.messages)

    # user = Users.query.filter_by(username=result["username"]).first()

    # if user is None or not user.check_password(result["password"]):
    #     return error_response(401, message="Invalid username or password")

    new_token = create_access_token(identity='id', fresh=True)
    payload = {"access_token": new_token}

    return jsonify(payload), 200

@bp.delete("/logout/token")
@jwt_required()
def logout_access_token():
    """
    Endpoint for revoking the current user"s access token
    Returns
    -------
    str
        A JSON object containing the sucess message
    """
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)


    return jsonify({"msg": "Successfully logged out"}), 200


@bp.delete("/logout/fresh")
@jwt_required(refresh=True)
def logout_refresh_token():
    """
    Endpoint for revoking the current user's refresh token
    Returns
    -------
    str
        A JSON object containing a success message
    """
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    return jsonify({"msg": "Successfully logged out"}), 200