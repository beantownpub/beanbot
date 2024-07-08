import json
import os

from flask import Response, request
from flask_restful import Resource
from api.libs.logging import init_logger
from api.libs.slack_modal import send_modal

LOG = init_logger(os.environ.get("LOG_LEVEL"))

class TimeoffRequestException(Exception):
    """Base  class for time off request exceptions exceptions"""


class TimeoffRequestAPI(Resource):

    def post(self):
        payload = json.loads(request.form.get('payload'))
        trigger_id = payload['trigger_id']
        send_modal(trigger_id)
        return Response(status=200)
