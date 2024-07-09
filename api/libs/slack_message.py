import requests
import json
import os

from datetime import datetime
from .logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))


#CHANNEL_ID = 'C031R2FQ34M'

def convert_date_to_words(raw_date):
    date_object = datetime.strptime(raw_date, "%Y-%m-%d")
    day_name = date_object.strftime("%a")
    date_month_year = date_object.strftime("%B %d, %Y")
    date_words = f"{day_name} {date_month_year}"
    return date_words


# Define the message payload
def build_approval_message(channel_id, username, start_date, end_date=None):
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
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Team Member:*\n{username}"
                    },
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
                "type": "actions",
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
    # start_date_words = convert_date_to_words(start_date)
    # end_date_words = convert_date_to_words(end_date)
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
                "text": {
                    "type": "mrkdwn",
                    "text": f":{emoji}: *This request has been {approval_status}*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ]
    }
    url = 'https://slack.com/api/chat.update'
    LOG.info('Update message: %s', message_payload)
    send_slack_request(url=url, message_payload=message_payload)

# Define the URL for the Slack API
def send_for_approval_message(channel_id, username, start_date, end_date=None):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    url = 'https://slack.com/api/chat.postMessage'
    message_payload = build_approval_message(channel_id=channel_id, username=username, start_date=start_date, end_date=end_date)
    send_slack_request(url=url, message_payload=message_payload)



def send_slack_request(url, message_payload):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    # Define the headers
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': f'Bearer {slack_bot_token}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(message_payload))
    LOG.info(response.status_code)
    LOG.info(response.json())
    return response.status_code
