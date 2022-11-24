from flask import Blueprint

bp = Blueprint("auth", __name__)

from app.routers.auth import routes
