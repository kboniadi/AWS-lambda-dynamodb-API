import asyncio

from aiohttp import ClientSession
from botocore.exceptions import ClientError
from flask import jsonify, request
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from app import db_instance
from app.domain.lawyers_domain import LawyersDomain, LawyersModel
from app.repository.lawyers_repository import LawyersRepository
from app.routers.errors.handlers import bad_request, error_response
from app.routers.lawyers import bp

lawyers_repository = LawyersRepository(db_instance)
lawyers_domain = LawyersDomain(lawyers_repository)

@bp.get("/")
def index_route():
    return 'Hello! Welcome to lawyers index route', 200

@bp.post("/create")
@jwt_required()
def create_lawyer(lawyers_model: LawyersModel):
    try:
        lawyers_domain.create_lawyer(lawyers_model)
        return (jsonify({"data": True}), 200)
    except ClientError:
        return error_response(500, "internal server error")

@bp.get("/get/<string:lawyer_email>")
# @jwt_required()
def get_lawyer(lawyer_email: str):
    try:
        response = lawyers_domain.get_lawyer(lawyer_email)
    except ClientError:
        return error_response(500, "internal server error")
    else:
        print(response)
        return (jsonify({"data": response}), 200) if response is not None else bad_request("No post found")

@bp.put("/update")
@jwt_required()
def update_lawyer(lawyers_model: LawyersModel):
    try:
        lawyers_domain.update_lawyer(lawyers_model)
        return (jsonify({"data": True}), 200)
    except ClientError:
        return error_response(500, "internal server error")

@bp.delete("/delete/<string:lawyer_email>")
# @jwt_required()
def delete_lawyer(lawyer_email: str):
    try:
        lawyers_domain.delete_lawyer(lawyer_email)
        return (jsonify({"data": True}), 200)
    except ClientError:
        return error_response(500, "internal server error")

@bp.get("/all")
# @jwt_required()
def get_all():
    try:
        response = lawyers_domain.get_all()
    except ClientError:
        return error_response(500, "internal server error")
    else:
        return (jsonify({"data": response}), 200) if response is not None else bad_request("No post found")