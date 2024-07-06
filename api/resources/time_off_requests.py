import json
import os

from flask import Response, request
from flask_restful import Resource
from api.libs.logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))

class TimeoffRequestException(Exception):
    """Base  class for time off request exceptions exceptions"""


class TimeoffRequestAPI(Resource):

    def post(self):
        LOG.info(json.loads(request.form.get('payload')))
        #time_off_request = request.get_data()
        #LOG.info(time_off_request)
        version = {"app": "beanbot", "version": "0.1.1"}
        return Response(version, mimetype="application/json", status=200)
