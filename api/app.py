import logging
import os
from flask import Flask
from flask_restful import Api

from api.libs.logging import init_logger
from api.resources.routes import init_routes


class BeanbotException(Exception):
    """Base class for beanbot exceptions"""

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
APP = Flask(__name__.split(".")[0], instance_path="/opt/app/api")
API = Api(APP)

LOG = init_logger(LOG_LEVEL)
LOG.info("Logging initialized | Level %s", LOG_LEVEL)
init_routes(API)
LOG.info("Routes initialized")
