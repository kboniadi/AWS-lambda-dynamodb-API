import os
from dotenv import load_dotenv

# Set base directory of the app
basedir = os.path.abspath(os.path.dirname(__file__))
# Load the .env and .flaskenv variables
load_dotenv(os.path.join(basedir, "../.env"))


class Config(object):
    """
    Set the config variables for the Flask app

    """

    SECRET_KEY = os.environ.get("SECRET_KEY")


    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    REDIS_URL = os.environ.get("REDIS_URL") or "redis://"
