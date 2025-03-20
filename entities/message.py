import json

from entities.error import ScriptError


class Message:
    def __init__(self, error: ScriptError):
        self.service_name = error.site
        self.element = error.element
        self.message = error.message
        self.string_search = error.string_search

    def __str__(self):
        embed = {
            "title": f"Erro em serviço {self.service_name}",
            "description": "O site apresentou um erro durante o monitoramento.",
            "color": 7506394,
            "footer": {
                "text": "Comunique-se com Rogerio Inacio em caso de problemas.",
            },
            "thumbnail": {
                "url": "https://images.icon-icons.com/2871/PNG/512/bot_robot_insect_icon_181890.png"
            },
            "fields": [
                {
                    "name": "Busca",
                    "value": self.string_search,
                    "inline": False
                },
                {
                    "name": "Elemento",
                    "value": self.element,
                    "inline": False
                },
                {
                    "name": "Mensagem",
                    "value": self.message,
                    "inline": False
                }
            ]
        }

        data = {
            "username": "Bot Monitor",
            "avatar_url": "https://images.icon-icons.com/2871/PNG/512/bot_robot_insect_icon_181890.png",
            "embeds": [embed],
        }

        return data