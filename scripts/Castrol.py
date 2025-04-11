import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from entities.error import ScriptError

class Castrol:
    def __init__(self, driver):
        self.driver = driver

    def run(self, text_search: str, first_run: bool):
        print("Iniciando busca no script Castrol para o texto: ", text_search)
        self.driver.get("https://www.castrol.com/pt_br/brazil/home/product-finder.html#/oil-selector")

        if first_run:
            try:
                WebDriverWait(self.driver, 90).until(EC.visibility_of_element_located((By.ID, "cookie-consent")))
                consent_button = self.driver.find_element(By.XPATH, "/html/body/div[9]/div/div/div/div/div/div[2]/div/div[2]/div[2]/div[2]/button")
                consent_button.click()

                cookie_button = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/button")
                cookie_button.click()

                time.sleep(2)
            except TimeoutException:
                script_error = ScriptError("Castrol", "Campo de busca", "TimeoutException", text_search)
                print(script_error)
                return script_error

        try:
            WebDriverWait(self.driver, 90).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/div/div/div[2]/div/div[2]/div")))
            oil_search = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/input")
            oil_search.send_keys(text_search)

            first_option = WebDriverWait(self.driver, 90).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/button")))
            first_option.click()

            search_button = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div/div/div/div[2]/div/div[2]/div/div/div/button[1]")
            search_button.click()

            time.sleep(3)
        except TimeoutException:
            script_error = ScriptError("Castrol", "Campo de busca", "TimeoutException", text_search)
            print(script_error)
            return script_error

        try:
            WebDriverWait(self.driver, 90).until(EC.visibility_of_element_located((By.CLASS_NAME, "mantine-Carousel-root")))
            result_list = self.driver.find_elements(By.XPATH, "/html/body/div[5]/div/div/div/div/div/div[2]/div/div[2]/div")

            if not result_list:
                script_error = ScriptError("Castrol", "Lista de óleos", "Sem itens retornados", text_search)
                print(script_error)
                return script_error

        except TimeoutException:
            script_error = ScriptError("Castrol", "Lista de óleos", "TimeoutException", text_search)
            print(script_error)
            return script_error
