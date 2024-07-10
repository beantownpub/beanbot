import requests
import json
import os

from datetime import datetime
from .logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))


SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


def convert_date_to_words(raw_date):
    date_object = datetime.strptime(raw_date, "%Y-%m-%d")
    day_name = date_object.strftime("%a")
    date_month_year = date_object.strftime("%B %d, %Y")
    date_words = f"{day_name} {date_month_year}"
    return date_words


def build_request_received_message(user_id, start_date, end_date):
    message_payload = {
        "channel": user_id,
        "text": "Time off request",
        "blocks": [
            {
                "type": "section",
                "block_id": "request-received",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Your timeoff request for `{convert_date_to_words(start_date)}` to `{convert_date_to_words(end_date)}` has been received and is awaiting approval. You'll receive another message once your request is updated*"
                }
            }
        ]
    }
    return message_payload


def build_user_approval_status_message(user_id, approval_status, text):
    if approval_status == "approved":
        emoji = "large_green_circle"
    if approval_status == "denied":
        emoji = "red_circle"
    message_payload = {
        "channel": user_id,
        "text": "Time off request",
        "blocks": [
            {
                "type": "section",
                "block_id": "request-received",
                "text": {
                    "type": "mrkdwn",
                    "text": f":{emoji}: *Your timeoff request has been {approval_status}*"
                }
            },
            {
                "type": "section",
                "block_id": "users-request-data",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{text}"
                }
            }
        ]
    }
    return message_payload


def build_approval_message(channel_id, username, start_date, details, end_date=None):
    start_date_words = convert_date_to_words(start_date)
    end_date_words = convert_date_to_words(end_date)
    message_payload = {
        "channel": channel_id,
        "text": "Time off request",
            "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Time Off Request",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "block_id": "username-field",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Team Member:*\n{username}"
                    }
                ]
            },
            {
                "type": "section",
                "block_id": "date-fields",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Start Date:*\n{start_date_words}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*End Date:*\n{end_date_words}"
                    }
                ]
            },
            {
                "type": "section",
                "block_id": "request-details",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Request Details*:\n>{details}"
                }
            },
            {
                "type": "actions",
                "block_id": "request-approval",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Approve"
                        },
                        "style": "primary",
                        "value": "approved"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Deny"
                        },
                        "style": "danger",
                        "value": "denied"
                    }
                ]
            }
        ]
    }
    return message_payload


def update_confirmation_message(channel_id, message_timestamp, username, text, approval_status):
    if approval_status == "approved":
        emoji = "large_green_circle"
    if approval_status == "denied":
        emoji = "red_circle"
    message_payload = {
        "channel": channel_id,
        "ts": message_timestamp,
        "text": "Time off request",
        "blocks": [
            {
                "type": "section",
                "block_id": "status-message",
                "text": {
                    "type": "mrkdwn",
                    "text": f":{emoji}: *This request has been {approval_status}*"
                }
            },
            {
                "type": "section",
                "block_id": "request-data",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{text}"
                }
            }
        ]
    }
    url = 'https://slack.com/api/chat.update'
    send_slack_post_request(url=url, message_payload=message_payload)


def send_user_approval_status_message(user_id, approval_status, text):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    url = 'https://slack.com/api/chat.postMessage'
    message_payload = build_user_approval_status_message(user_id=user_id, approval_status=approval_status, text=text)
    send_slack_post_request(url=url, message_payload=message_payload)


def send_request_received_confirmation_to_user(user_id, start_date, end_date):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    url = 'https://slack.com/api/chat.postMessage'
    message_payload = build_request_received_message(user_id=user_id, start_date=start_date, end_date=end_date)
    send_slack_post_request(url=url, message_payload=message_payload)


def send_for_approval_message(channel_id, username, details, start_date, end_date=None):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    url = 'https://slack.com/api/chat.postMessage'
    message_payload = build_approval_message(channel_id=channel_id, username=username, details=details, start_date=start_date, end_date=end_date)
    send_slack_post_request(url=url, message_payload=message_payload)


def send_slack_get_request(url):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching users list: {response.status_code}, {response.text}")

    return response.json()


def send_slack_post_request(url, message_payload):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(message_payload))
    #LOG.info(f"Slack POST response: {response.status_code}")
    #LOG.info(json.dumps(response.json(),  indent=2))
    return response.status_code
