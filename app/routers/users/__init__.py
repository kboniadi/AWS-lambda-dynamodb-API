from flask import Blueprint

bp = Blueprint("users", __name__)

from app.routers.users import routes
