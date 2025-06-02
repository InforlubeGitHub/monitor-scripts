import json

import requests

from entities.message import Message


class LambdaNotification:
    def __init__(self, lambda_url) -> None:
        self.lambda_url = lambda_url

    def send(self, message: Message) -> None:
        content = json.dumps({
            "service_name": message.service_name,
            "element": message.element,
            "message": message.message,
            "string_search": message.string_search,
            "name": "Problema identificado em monitoramento",
        })

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(self.lambda_url, data=content, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to send notification: {response.status_code} - {response.text}")
        else:
            print("Notification sent successfully")