import time
import random
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from entities.error import ScriptError

class TotalEnergies:
    def __init__(self, driver):
        self.driver = driver

    def run(self, text_search: str):
        print("Iniciando busca no script TotalEnergies para o texto: ", text_search)
        self.driver.get("https://lubconsult.dafitech.com/")

        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "LiteralSearchInput")))

        search_input = self.driver.find_element(By.ID, "LiteralSearchInput")
        actions = ActionChains(self.driver)
        actions.move_to_element(search_input).click().perform()
        time.sleep(0.5)

        search_input.clear()
        time.sleep(0.5)

        for char in text_search:
            search_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        time.sleep(1)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "LiteralSearchList"))
            )
            print("Search results loaded successfully")
        except TimeoutException:
            script_error = ScriptError("TotalEnergies", "Lista de resultados de carros", "TimeoutException", text_search)
            print(script_error)
            return script_error

        time.sleep(0.5)

        first_result = self.driver.find_element(By.CSS_SELECTOR, ".search-literal-list-item")
        print(f"Found first result: {first_result.get_attribute('data-display')}")

        actions.move_to_element(first_result).pause(random.uniform(0.3, 0.7)).click().perform()

        print("Clicked on the first search result")

        search_button = self.driver.find_element(By.ID, "LiteralSearchFind")

        actions.move_to_element(search_button).pause(random.uniform(0.3, 0.7)).click().perform()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "Catalog"))
            )
            print("Catalog loaded successfully")
        except TimeoutException:
            script_error = ScriptError("TotalEnergies", "Catalog", "TimeoutException", text_search)
            print(script_error)
            return script_error

        time.sleep(5)