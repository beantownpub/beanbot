import json
import os
import re

from flask import Response, request
from flask_restful import Resource
from api.libs.logging import init_logger
from api.libs.slack_modal import send_modal
from api.libs.slack_message import send_for_approval_message, update_confirmation_message

LOG = init_logger(os.environ.get("LOG_LEVEL"))

class TimeoffRequestException(Exception):
    """Base  class for time off request exceptions exceptions"""


def process_view_submission(payload):
    username = payload["user"]["username"]
    #user_id = payload["user"]["id"]
    channel_id = "C07C69B7XNC"
    start_date = payload["view"]["state"]["values"]["start-date"]["datepicker-start"]["selected_date"]
    end_date = payload["view"]["state"]["values"]["end-date"]["datepicker-end"]["selected_date"]
    if start_date == end_date:
        end_date = None
    send_for_approval_message(channel_id=channel_id, username=username, start_date=start_date, end_date=end_date)

def update_approval_message(payload):
    username = payload["user"]["username"]
    user_id = payload["user"]["id"]
    if payload["container"]["type"] == "message":
        text_list = []
        if len(payload["actions"]) == 1:
            for block in payload["message"]["blocks"]:
                if block["type"] == "section":
                    for field in block["fields"]:
                        text_list.append(field["text"])
            approval_status = payload["actions"][0]["value"]
            message_timestamp = payload["container"]["message_ts"]
            channel_id = payload["container"]["channel_id"]
            update_confirmation_message(channel_id=channel_id, message_timestamp=message_timestamp, username=username, text="\n".join(text_list), approval_status=approval_status)


def get_username_from_text(text_string):
    pattern = r'[*]?(.*)$'
    match = re.search(pattern, text_string)
    if match:
        return match.groups()[0]


class TimeoffRequestAPI(Resource):

    def post(self):
        payload = json.loads(request.form.get('payload'))
        LOG.info(json.dumps(payload, indent=2))
        if payload["type"] == "shortcut":
            trigger_id = payload['trigger_id']
            send_modal(trigger_id)
        if payload["type"] == "view_submission":
            process_view_submission(payload)
        if payload["type"] == "block_actions":
            update_approval_message(payload)

        return Response(status=200)
