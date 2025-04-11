import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from entities.error import ScriptError

class Lubel:
    def __init__(self, driver):
        self.driver = driver
        self.retries = 10

    def run(self):
        print("Iniciando busca no script Lubel")
        self.driver.get("https://www.moura.com.br/produtos/lubel")

        for attempt in range(self.retries):
            try:
                WebDriverWait(self.driver, 90).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cc-message-container")))
                consent_button = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/a[2]")

                consent_button.click()
                return None
            except TimeoutException:
                if attempt < self.retries:
                    script_error = ScriptError("Lubel", "Cookie Dialog", "TimeoutException", "")
                    print(script_error)
                    return script_error
                else:
                    self.retries -= 1

        self.retries = 10

        for attempt in range(self.retries):
            try:
                know_oils_button = self.driver.find_element(By.CLASS_NAME, "chakra-button")

                know_oils_button.click()

                catalog_pdf_button = self.driver.find_element(By.CLASS_NAME, "css-z8c6fa")

                catalog_pdf_button.click()

                time.sleep(3)

                print("Script para Lubel finalizada com sucesso")

                return None

            except Exception as e:
                if attempt < self.retries:
                    script_error = ScriptError("Lubel", "Catalog PDF", f"Exception não identificada. Detalhes: {e}", "")
                    print(script_error)
                    return script_error
                else:
                    self.retries -= 1

