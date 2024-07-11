import json
import os
import re

from flask import Response, request
from flask_restful import Resource
from api.libs.logging import init_logger
from api.libs.slack_modal import send_modal
from api.libs.slack_message import (
  send_for_approval_message,
  update_confirmation_message,
  send_request_received_confirmation_to_user,
  send_user_approval_status_message
)
from api.libs.utils import (
  convert_date_to_timestamp,
  get_username_from_text,
  get_users_id,
  get_users_real_name,
  get_users_title
)

LOG = init_logger(os.environ.get("LOG_LEVEL"))


class TimeoffRequestException(Exception):
    """Base  class for time off request exceptions exceptions"""


def _process_view_submission(payload):
  user_id = payload["user"]["id"]
  username = get_users_real_name(user_id)
  title = get_users_title(user_id)
  LOG.debug("Title: %s", title)
  channel_id = "C07C69B7XNC"
  details = payload["view"]["state"]["values"]["request-details"]["request-details"]["value"]
  start_date = payload["view"]["state"]["values"]["start-date"]["datepicker-start"]["selected_date"]
  end_date = payload["view"]["state"]["values"]["end-date"]["datepicker-end"]["selected_date"]
  if start_date == end_date:
    end_date = None
  if convert_date_to_timestamp(start_date) > convert_date_to_timestamp(end_date):
    raise TimeoffRequestException("Error start cannot be after end date")
  send_for_approval_message(channel_id=channel_id, username=username, position=title, details=details, start_date=start_date, end_date=end_date)
  send_request_received_confirmation_to_user(user_id=user_id, start_date=start_date, end_date=end_date)


def _process_message(payload):
  username = payload["user"]["username"]
  user_id = payload["user"]["id"]
  if payload["container"]["type"] == "message":
    text_list = []
    users_real_name = ""
    if len(payload["actions"]) == 1:
      for block in payload["message"]["blocks"]:
        if block["block_id"] == "username-field":
          users_real_name = get_username_from_text(block["fields"][0]["text"])
          text_list.append(block["fields"][0]["text"])
          text_list.append(block["fields"][1]["text"])
        if block["block_id"] == "date-fields":
            for field in block["fields"]:
              text_list.append(field["text"])
        if block["block_id"] == "request-details":
            text_list.append(block["text"]["text"])
      # Remove "Team Member" line when sending direct message to that user
      user_text_list = text_list.copy()
      user_text_list.pop(0)
      # Remove "Position" line when sending direct message to that user
      user_text_list.pop(0)
      user_id = get_users_id(real_name=users_real_name)
      approval_status = payload["actions"][0]["value"]
      message_timestamp = payload["container"]["message_ts"]
      channel_id = payload["container"]["channel_id"]
      update_confirmation_message(channel_id=channel_id, message_timestamp=message_timestamp, username=username, text="\n".join(text_list), approval_status=approval_status)
      send_user_approval_status_message(user_id=user_id, text="\n".join(user_text_list), approval_status=approval_status)


class TimeoffRequestAPI(Resource):

  def post(self):
    payload = json.loads(request.form.get('payload'))
    LOG.debug(json.dumps(payload, indent=2))
    if payload["type"] == "shortcut":
      trigger_id = payload['trigger_id']
      send_modal(trigger_id)
    if payload["type"] == "view_submission":
      _process_view_submission(payload)
    if payload["type"] == "block_actions":
      _process_message(payload)

    return Response(status=200)

