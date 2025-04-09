import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from entities.error import ScriptError

class Lubel:
    def __init__(self, driver):
        self.driver = driver

    def run(self):
        print("Iniciando busca no script Lubel")
        self.driver.get("https://www.moura.com.br/produtos/lubel")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cc-message-container")))
            consent_button = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/a[2]")

            consent_button.click()
        except TimeoutException:
            script_error = ScriptError("Lubel", "Cookie Dialog", "TimeoutException", "")
            print(script_error)
            return script_error

        know_oils_button = self.driver.find_element(By.CLASS_NAME, "chakra-button")

        know_oils_button.click()

        catalog_pdf_button = self.driver.find_element(By.CLASS_NAME, "css-z8c6fa")

        catalog_pdf_button.click()

        time.sleep(3)

        print("Script para Lubel finalizada com sucesso")

