from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from entities.error import ScriptError


class Lubrax:
    def __init__(self, driver):
        self.driver = driver

    def run(self, text_search: str, first_run: bool):
        print("Iniciando busca no script Lubrax para o texto: ", text_search)
        self.driver.get("https://www.lubrax.com.br/descubra-qual-o-melhor-oleo-para-o-seu-motor")

        if first_run:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
                consent_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")

                consent_button.click()
            except TimeoutException:
                script_error = ScriptError("Lubrax", "Cookie Dialog", "TimeoutException", text_search)
                print(script_error)
                return script_error

        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "input-search")))
            oil_search = self.driver.find_element(By.ID, "input-search")
            oil_search.send_keys(text_search)
        except TimeoutException:
            script_error = ScriptError("Lubrax", "Campo de busca", "TimeoutException", text_search)
            print(script_error)
            return script_error

        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "scrollableDiv")))

            result_list = self.driver.find_elements(By.XPATH,
                                                    "//div[@id='scrollableDiv']//div[contains(@class, 'infinite-scroll-component')]/div")
        except TimeoutException:
            script_error = ScriptError("Lubrax", "Lista de óleos", "TimeoutException", text_search)
            print(script_error)
            return script_error

        if result_list:
            first_vehicle = result_list[0]

            first_vehicle.click()
        else:
            script_error = ScriptError("Lubrax", "Lista de óleos", "Sem itens retornados", text_search)
            print(script_error)
            return script_error

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'sc-cCcYRi')]/div")))

        product_containers = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-cCcYRi')]/div")

        if product_containers:
            print(f"Produtos identificados para o veículo {text_search}")
        else:
            print("No products found")

        print("Finalizando busca no script Lubrax para o texto: ", text_search)