from datetime import datetime

import schedule
import time

from entities.config import Config
from entities.error import ScriptError
from entities.message import Message
from notification.discord import Discord
from scripts.Lubel import Lubel
from scripts.Lubrax import Lubrax
from scripts.Castrol import Castrol
from scripts.TotalEnergies import TotalEnergies

def main():
    print("Iniciando monitoramento...")

    config = Config()
    config.load()
    config.show()

    schedule.every(config.interval).minutes.do((lambda: run_scripts(config)))

    run_scripts(config)

    while True:
        schedule.run_pending()
        time.sleep(1)

def run_scripts(config: Config = None):
    now = datetime.now()
    print(f"Rodando monitoramento as {now}")

    discord_instance = Discord(
        "https://discordapp.com/api/webhooks/1364673256631566510/V1RQwnSwAlyeZoKVn2YPW8kwII4ZlaeZRUHKexvFERn3-035lCOYM6mVqBstz5W6kDPX")

    errors = []

    scenarios = [
        "Renault Duster 2020 2.0",
        "Renault Fluence 2017",
        "Honda Civic 2018 2.0"
    ]

    lubel = Lubel(config.lubel_api_key)

    for scenario in scenarios:
        try:
            lubel.run(scenario)
        except ScriptError as e:
            errors.append(e)
        except Exception as e:
            script_error = ScriptError("Lubel", "Search", f"{e.__str__()}", "")
            print(script_error)
            errors.append(script_error)

    for error in errors:
        discord_instance.send(Message(error))

    print("Monitoramento finalizado com sucesso")

if __name__ == '__main__':
    main()
