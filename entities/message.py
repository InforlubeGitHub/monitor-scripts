import json


class Message:
    def __init__(self, service_name: str, content: str):
        self.service_name = service_name
        self.content = content

    def __str__(self):
        embed = {
            "title": "Erro em monitoramento",
            "description": "O site apresentou um erro durante o monitoramento.",
            "color": 7506394,  # Hex color code converted to decimal
            "footer": {
                "text": "Created by Inforlube",
            },
            "thumbnail": {
                "url": "https://images.icon-icons.com/2871/PNG/512/bot_robot_insect_icon_181890.png"
            },
            "fields": [
                {
                    "name": "Site: " + self.service_name,
                    "value": "Erro: " + self.content,
                    "inline": True
                },
            ]
        }

        data = {
            "username": "Bot Monitor",  # Optional: custom name for your webhook
            "avatar_url": "https://images.icon-icons.com/2871/PNG/512/bot_robot_insect_icon_181890.png",  # Optional: custom avatar # Regular message content
            "embeds": [embed],  # You can include multiple embeds in one message
        }

        return data