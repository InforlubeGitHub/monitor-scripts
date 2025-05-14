from datetime import datetime

import schedule
import time

from entities.error import ScriptError
from entities.message import Message
from notification.discord import Discord
from scripts.Lubel import Lubel
from scripts.Lubrax import Lubrax
from scripts.Castrol import Castrol
from scripts.TotalEnergies import TotalEnergies
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    print("Iniciando monitoramento...")
    schedule.every(2).minutes.do(run_scripts)

    run_scripts()

    while True:
        schedule.run_pending()
        time.sleep(1)

def load_variables():
    try:
        lubel_api_key = os.getenv("LUBEL_API_KEY")
        if not lubel_api_key:
            raise ValueError("LUBEL_API_KEY não encontrado nas variáveis de ambiente.")
        return lubel_api_key
    except Exception as e:
        print(f"Erro ao carregar variáveis de ambiente: {e}")
        raise

def run_scripts():
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

    lubel_api_key = load_variables()

    lubel = Lubel(lubel_api_key)

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
