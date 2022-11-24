from flask import request, jsonify

from app.routers.lawyers import bp
from app.routers.errors.handlers import bad_request

from flask_jwt_extended import jwt_required, current_user

from marshmallow import ValidationError

import asyncio
from aiohttp import ClientSession

from app import db_instance
from app.domain.lawyers_domain import LawyersDomain, LawyersModel
from app.repository.lawyers_repository import LawyersRepository

lawyers_repository = LawyersRepository(db_instance)
lawyers_domain = LawyersDomain(lawyers_repository)

@bp.get("/")
def index_route() -> str:
    return 'Hello! Welcome to lawyers index route'

@bp.post("/create")
def create_lawyer(lawyers_model: LawyersModel):
    return lawyers_domain.create_lawyer(lawyers_model)

@bp.get("/get/<string:lawyer_email>")
def get_lawyer(lawyer_email: str):
    try:
        return lawyers_domain.get_lawyer(lawyer_email)
    except KeyError:
        return bad_request("No post found")

@bp.put("/update")
def update_lawyer(lawyers_model: LawyersModel):
    return lawyers_domain.update_lawyer(lawyers_model)

@bp.delete("/delete/<string:lawyer_email>")
def delete_lawyer(lawyer_email: str):
    return lawyers_domain.delete_lawyer(lawyer_email)

@bp.get("/all")
def get_all():
    return jsonify({"data": lawyers_domain.get_all()})