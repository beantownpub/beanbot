import json
import os
import re
from datetime import datetime

from .slack_message import send_slack_get_request
from .logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))

def _get_users(url):
    return send_slack_get_request(url)["members"]

USERS = _get_users('https://slack.com/api/users.list')

def add_creation_date(message_body):
    created = datetime.strftime(datetime.today(), "%m-%d-%Y %H:%M")
    message_body["created"] = created
    return message_body


def get_username_from_text(text_string):
    LOG.info("Text String: %s", text_string)
    pattern = r'[*]?(.*)$'
    match = re.search(pattern, text_string)
    if match:
        LOG.info(match.groups())
        return match.groups()[0]


def get_users_id(real_name):
    for user in USERS:
        if user["real_name"] == real_name:
            return user["id"]


def get_users_title(user_id):
    for user in USERS:
        if user["id"] == user_id:
            return user["profile"]["title"]


def get_users_real_name(user_id):
    for user in USERS:
        if user["id"] == user_id:
            return user["real_name"]


def convert_date_to_timestamp(date_string):
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    # Convert the datetime object into a timestamp (seconds since the epoch)
    timestamp = date_object.timestamp()

    return timestamp
