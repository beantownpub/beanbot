import datetime
import json
import os
import requests

from .logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))


def make_modal(trigger_id):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    modal_view = {
        "response_action": "push",
        "trigger_id": f"{trigger_id}",
        "view": {
            "type": "modal",
            "callback_id": "request-time-off",
            "title": {
                "type": "plain_text",
                "text": "Request time off"
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
                            "emoji": True
                        },
                        "action_id": "datepicker-start"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "initial_date": f"{current_year}-{current_month}-1",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an end date",
                            "emoji": True
                        },
                        "action_id": "datepicker-end"
                    }
                }
            ]
        }
    }

# Make the request to open the modal
def send_modal(trigger_id):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    modal_view = make_modal(trigger_id)
    response = requests.post(
        'https://slack.com/api/views.open',
        headers={
            'Authorization': f'Bearer {slack_bot_token}',
            'Content-Type': 'application/json;charset=utf-8'
        },
        data=json.dumps(modal_view)
    )
    is_json = response.json().get('ok')
    LOG.info(dir(response))
    LOG.info(response.text)
    LOG.info(response.content)
    LOG.info(f'Status code: {response.status_code} JSON: {is_json}')

