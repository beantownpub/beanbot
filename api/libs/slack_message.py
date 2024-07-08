import requests
import json
import os

from .logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))


#CHANNEL_ID = 'C031R2FQ34M'

# Define the message payload
def build_approval_message(channel_id, username, start_date, end_date=None):
    if not end_date:
        requested_dates = f"The requested date {start_date}"
    else:
        requested_dates = f"The requested are *{start_date}* to *{end_date}*"
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
                        "text": f"*Team member {username} has requested timeoff*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": requested_dates
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
                        "value": "time_off_approved"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Deny"
                        },
                        "style": "danger",
                        "value": "time_off_denied"
                    }
                ]
            }
        ]
    }
    return message_payload

def update_confirmation_message(channel_id, message_timestamp, username, approval_status):
    message_payload = {
        "channel": channel_id,
        "ts": message_timestamp,
        "text": "Time off request",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*The timeoff request for {username} has been {approval_status}*"
                }
            }
        ]
    }
    url = 'https://slack.com/api/chat.update'
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
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {slack_bot_token}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(message_payload))
    LOG.info(response.status_code)
    LOG.info(response.json())
    return response.status_code
