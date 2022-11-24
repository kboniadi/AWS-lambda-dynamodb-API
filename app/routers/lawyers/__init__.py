from flask import Blueprint

bp = Blueprint("lawyers", __name__)

from app.routers.lawyers import routes
