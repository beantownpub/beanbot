import json
import os

from flask import Response, request
from flask_restful import Resource
from api.libs.logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))

class TimeoffRequestException(Exception):
    """Base  class for time off request exceptions exceptions"""


class TimeoffRequestAPI(Resource):

    def get(self):
        LOG.info("GET")
        LOG.info(dir(request))
        time_off_request = request.get_json()
        LOG.info(time_off_request)
        version = {"app": "beanbot", "version": "0.1.1", "time_off_request": order}
        return Response(version, mimetype="application/json", status=200)

    def post(self):
        LOG.info("POST")
        LOG.info(dir(request))
        time_off_request = request.get_json()
        LOG.info(time_off_request)
        version = {"app": "beanbot", "version": "0.1.1"}
        return Response(version, mimetype="application/json", status=200)
