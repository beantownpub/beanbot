import datetime
import json
import os
import requests

from .logging import init_logger

LOG = init_logger(os.environ.get("LOG_LEVEL"))


def build_modal(trigger_id):
    current_time = datetime.datetime.now()
    current_year = current_time.year
    current_month = current_time.month
    current_day  = current_time.day

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
                        "text": "*Select a start date*"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "initial_date": f"{current_year}-{current_month}-{current_day}",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a start date",
                            "emoji": True
                        },
                        "action_id": "datepicker-start"
                    }
                },
                {
                    "type": "section",
                    "block_id": "end-date",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Select an end date*"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "initial_date": f"{current_year}-{current_month}-{current_day}",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an end date",
                            "emoji": True
                        },
                        "action_id": "datepicker-end"
                    }
                },
                {
                    "type": "input",
                    "block_id": "request-details",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "request-details"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Request Details",
                        "emoji": True
                    }
                }
            ]
        }
    }
    return modal_view


def send_modal(trigger_id):
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    modal_view = build_modal(trigger_id)
    response = requests.post(
        'https://slack.com/api/views.open',
        headers={
            'Authorization': f'Bearer {slack_bot_token}',
            'Content-Type': 'application/json;charset=utf-8'
        },
        data=json.dumps(modal_view)
    )
    #is_json = response.json().get('ok')
    #LOG.info('Modal Response: %s', json.dumps(response.json(), indent=2))

