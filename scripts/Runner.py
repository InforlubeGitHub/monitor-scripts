import requests

from entities.error import ScriptError

class Runner:
    def __init__(self, service_name: str, api_key: str, api_url: str) -> None:
        self.service_name = service_name
        self.api_key = api_key
        self.api_url = api_url
        self.auth = None

    def run(self, vehicle: str) -> None:
        print(f"Iniciando busca no script {self.service_name} para o veículo: ", vehicle)

        try:
            self.login()
            ticket, model = self.search_model(vehicle)
            self.search_products(ticket, model)
        except ScriptError as e:
            raise e


    def login(self) -> None:
        try:
            response = requests.get(
                f"{self.api_url}/Auth",
                headers={
                    "accept": "application/problem+json",
                    "credentials": f"{self.api_key}",
                }
            )

            response.raise_for_status()

            response_body = response.json()

            self.auth = response_body["Jwt"]
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                script_error = ScriptError(self.service_name, "Login", "Unauthorized", "")
                print(script_error)
                raise script_error
            else:
                script_error = ScriptError(self.service_name, "Login", f"{e.__str__()}", "")
                print(script_error)
                raise script_error
        except Exception as e:
            script_error = ScriptError(self.service_name, "Login", f"{e.__str__()}", "")
            print(script_error)
            raise script_error

    def search_model(self, vehicle: str) -> tuple[str, str] | None:
        try:
            response = requests.get(
                f"{self.api_url}/Models?UsePartialWords=true&SpellCheck=true&SearchText={vehicle}&PageSize=10&CurrentPage=1&IsPaged=true",
                headers={
                    "accept": "application/problem+json",
                    "authorization": f"Bearer {self.auth}",
                },
                params={
                    "search": vehicle
                }
            )

            response.raise_for_status()

            response_body = response.json()

            headers = response.headers

            ticket = headers["ticket"]
            model_id = response_body[0]["Id"]

            return ticket, model_id
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                script_error = ScriptError(self.service_name, "Search", "Unauthorized", vehicle)
                print(script_error)
                raise script_error
            else:
                script_error = ScriptError(self.service_name, "Search", f"{e.__str__()}", vehicle)
                print(script_error)
                raise script_error
        except Exception as e:
            script_error = ScriptError(self.service_name, "Search", f"{e.__str__()}", vehicle)
            print(script_error)
            raise script_error

    def search_products(self, ticket, vehicle) -> None:
        try:
            response = requests.get(
                f"{self.api_url}/Products/Recommendation/Model/{vehicle}",
                headers={
                    "accept": "application/problem+json",
                    "authorization": f"Bearer {self.auth}",
                    "Ticket": f"{ticket}",
                }
            )

            response.raise_for_status()

            response_body = response.json()
            components = response_body["Components"]

            if not components:
                script_error = ScriptError(self.service_name, "Products Search", "No products found", vehicle)
                print(script_error)
                raise script_error
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                script_error = ScriptError(self.service_name, "Products Search", "Unauthorized", vehicle)
                print(script_error)
                raise script_error
            else:
                script_error = ScriptError(self.service_name, "Products Search", f"{e.__str__()}", vehicle)
                print(script_error)
                raise script_error
        except Exception as e:
            script_error = ScriptError(self.service_name, "Products Search", f"{e.__str__()}", vehicle)
            print(script_error)
            raise script_error