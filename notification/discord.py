import requests
import entities.message as Message

class Discord:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: Message):
        content = message.__str__()
        result = requests.post(self.webhook_url, json=content)

        if result.status_code != 200:
            print(result.status_code)
            print(result.text)