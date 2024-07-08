import datetime
import json
import os
import requests

from .logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))


def make_modal():
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    modal_view = {
        "type": "modal",
        "callback_id": "modal-identifier",
        "title": {
            "type": "plain_text",
            "text": "Time Off Request"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "blocks": [
            {
                "type": "section",
                "block_id": "start-date",
                "text": {
                    "type": "mrkdwn",
                    "text": "Request some fuckin time off!"
                },
                "accessory": {
                    "type": "datepicker",
                    "initial_date": f"{current_year}-{current_month}-1",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a start date",
                        "emoji": true
                    },
                    "action_id": "datepicker-start"
                },
                "accessory": {
                    "type": "datepicker",
                    "initial_date": f"{current_year}-{current_month}-1",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an end date",
                        "emoji": true
                    },
                    "action_id": "datepicker-end"
                }
            }
        ]
    }

# Make the request to open the modal
def send_modal(trigger_id):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    modal_view = make_modal()
    response = requests.post(
        'https://slack.com/api/views.open',
        headers={
            'Authorization': f'Bearer {slack_bot_token}',
            'Content-Type': 'application/json;charset=utf-8'
        },
        data=json.dumps({
            "trigger_id": trigger_id,
            "view": modal_view
        })
    )
    if response.status_code == 200 and response.json().get('ok'):
        LOG.info("Modal opened successfully!")
    else:
        LOG.info("Failed to open modal:", response.json())
