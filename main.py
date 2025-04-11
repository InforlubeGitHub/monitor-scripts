from datetime import datetime

import schedule
import time

from selenium import webdriver

from entities.error import ScriptError
from entities.message import Message
from notification.discord import Discord
from scripts.Lubel import Lubel
from scripts.Lubrax import Lubrax
from scripts.Castrol import Castrol
from selenium.webdriver.firefox.options import Options

from scripts.TotalEnergies import TotalEnergies


def main():
    print("Iniciando monitoramento...")
    schedule.every(30).minutes.do(run_scripts)

    run_scripts()

    while True:
        schedule.run_pending()
        time.sleep(1)

def run_scripts():
    now = datetime.now()
    print(f"Rodando monitoramento as {now}")

    discord_instance = Discord(
        "https://discordapp.com/api/webhooks/1351560228147167262/zhmZJacoissnC_ux-WuLHqfg8DrnS9Q8yxDnyBKAJJKkhiOrSFH_NQwIFQ-6MkqWB-kI")

    options = Options()

    '''chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")'''

    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-content")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Firefox(options=options)

    errors = []

    scenarios = [
        "Renault Duster 2020 2.0",
        "Renault Fluence 2017",
        "Honda Civic 2018 2.0"
    ]

    try:
        errors += run_lubrax_script(driver, scenarios)
    except Exception as e:
        error = ScriptError("Lubrax", "Desconhecido", f"Exception não identificada. Detalhes: {e}", "")
        print(f"Erro durante o monitoramento do Lubrax. Detalhes: {e}")
        errors.append(error)


    try:
        errors += run_total_energies_script(driver, scenarios)
    except Exception as e:
        error = ScriptError("TotalEnergies", "Desconhecido", f"Exception não identificada. Detalhes: {e}", "")
        print(f"Erro durante o monitoramento do TotalEnergies. Detalhes: {e}")
        errors.append(error)

    try:
        errors += run_castrol_script(driver, scenarios)
    except Exception as e:
        error = ScriptError("Castrol", "Desconhecido", f"Exception não identificada. Detalhes: {e}", "")
        print(f"Erro durante o monitoramento do Castrol. Detalhes: {e}")
        errors.append(error)

    try:
        errors += run_lubel_script(driver)
    except Exception as e:
        error = ScriptError("Lubel", "Desconhecido", f"Exception não identificada. Detalhes: {e}", "")
        print(f"Erro durante o monitoramento do Lubel. Detalhes: {e}")
        errors.append(error)


    for error in errors:
        message = Message(error)

        try:
            discord_instance.send(message)
        except Exception as e:
            print(f"Erro ao enviar notificação ao Discord. Detalhes: {e}")


    driver.close()

    print("Monitoramento finalizado com sucesso")

def run_lubrax_script(driver, scenarios):
    print("Iniciando busca no script Lubrax")
    lubrax = Lubrax(driver)

    errors = []

    first_run = True

    for scenario in scenarios:
        error = lubrax.run(scenario, first_run)

        first_run = False

        if error:
            errors.append(error)

    return errors

def run_total_energies_script(driver, scenarios):
    print("Iniciando busca no script TotalEnergies")
    total_energies = TotalEnergies(driver)

    errors = []

    for scenario in scenarios:
        error = total_energies.run(scenario)

        if error:
            errors.append(error)

    return errors

def run_castrol_script(driver, scenarios):
    print("Iniciando busca no script Castrol")
    castrol = Castrol(driver)

    errors = []

    first_run = True

    for scenario in scenarios:
        error = castrol.run(scenario, first_run)

        if error:
            errors.append(error)

        first_run = False

    return errors

def run_lubel_script(driver):
    lubel = Lubel(driver)

    errors = []

    error = lubel.run()

    if error:
        errors.append(error)

    return errors


if __name__ == '__main__':
    main()

