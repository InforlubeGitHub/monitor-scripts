from datetime import datetime

import schedule
import time

from entities.config import Config
from notification.discord import Discord
from notification.lambda_notification import LambdaNotification
from scripts.Runner import Runner

def main():
    print("Iniciando monitoramento...")

    config = Config()
    config.load()
    config.show()

    discord_instance = Discord(config.discord_webhook)
    lambda_instance = LambdaNotification(config.monitor_lambda)

    runners = []

    lubel = Runner("Lubel", config.lubel_api_key, config.lubel_api_url, discord_instance, lambda_instance)
    castrol = Runner("Castrol", config.castrol_api_key, config.castrol_api_url, discord_instance, lambda_instance)
    total_energies = Runner("TotalEnergies", config.totalenergies_api_key, config.totalenergies_api_url, discord_instance, lambda_instance)
    mobil = Runner("Mobil", config.mobil_api_key, config.mobil_api_url, discord_instance, lambda_instance)

    runners.append(lubel)
    runners.append(castrol)
    runners.append(total_energies)
    runners.append(mobil)

    schedule.every(config.interval).minutes.do((lambda: run_scripts(runners)))

    run_scripts(runners)

    while True:
        schedule.run_pending()
        time.sleep(1)

def run_scripts(runners: list[Runner]) -> None:
    now = datetime.now()
    print(f"Rodando monitoramento as {now}")

    for runner in runners:
        runner.run()

    print("Monitoramento finalizado com sucesso")

if __name__ == '__main__':
    main()
