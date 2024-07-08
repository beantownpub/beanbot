import json
import os

from flask import Response, request
from flask_restful import Resource
from api.libs.logging import init_logger
from api.libs.slack_modal import send_modal
from api.libs.slack_message import send_message

LOG = init_logger(os.environ.get("LOG_LEVEL"))

class TimeoffRequestException(Exception):
    """Base  class for time off request exceptions exceptions"""


def process_view_submission(payload):
    username = payload["user"]["username"]
    user_id = payload["user"]["id"]
    start_date = payload["view"]["state"]["values"]["start-date"]["datepicker-start"]["selected_date"]
    end_date = payload["view"]["state"]["values"]["end-date"]["datepicker-end"]["selected_date"]
    if start_date == end_date:
        end_date = None
    send_message(channel_id=user_id, username=username, start_date=start_date, end_date=end_date)

class TimeoffRequestAPI(Resource):

    def post(self):
        payload = json.loads(request.form.get('payload'))
        LOG.info(payload)
        if payload["type"] == "shortcut":
            trigger_id = payload['trigger_id']
            send_modal(trigger_id)
        if payload["type"] == "view_submission":
            process_view_submission(payload)

        return Response(status=200)
