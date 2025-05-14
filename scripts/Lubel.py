import requests

from entities.error import ScriptError

class Lubel:
    def __init__(self, api_key):
        self.retries = 10
        self.api_key = api_key
        self.auth = None

    def run(self, vehicle: str) -> None:
        print("Iniciando busca no script Lubel para o veículo: ", vehicle)

        try:
            self.login()
            ticket, model = self.search_model(vehicle)
            self.search_products(ticket, model)
        except ScriptError as e:
            raise e


    def login(self) -> None:
        try:
            response = requests.get(
                "https://api.dafitech.com/api/v2/Auth",
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
                script_error = ScriptError("Lubel", "Login", "Unauthorized", "")
                print(script_error)
                raise script_error
            else:
                script_error = ScriptError("Lubel", "Login", f"{e.__str__()}", "")
                print(script_error)
                raise script_error
        except Exception as e:
            script_error = ScriptError("Lubel", "Login", f"{e.__str__()}", "")
            print(script_error)
            raise script_error

    def search_model(self, vehicle: str) -> tuple[str, str] | None:
        try:
            response = requests.get(
                f"https://api.dafitech.com/api/v2/Models?UsePartialWords=true&SpellCheck=true&SearchText={vehicle}&PageSize=10&CurrentPage=1&IsPaged=true",
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
                script_error = ScriptError("Lubel", "Search", "Unauthorized", vehicle)
                print(script_error)
                raise script_error
            else:
                script_error = ScriptError("Lubel", "Search", f"{e.__str__()}", vehicle)
                print(script_error)
                raise script_error
        except Exception as e:
            script_error = ScriptError("Lubel", "Search", f"{e.__str__()}", vehicle)
            print(script_error)
            raise script_error

    def search_products(self, ticket, vehicle) -> None:
        try:
            response = requests.get(
                f"https://api.dafitech.com/api/v2/Products/Recommendation/Model/{vehicle}",
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
                script_error = ScriptError("Lubel", "Products Search", "No products found", vehicle)
                print(script_error)
                raise script_error
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                script_error = ScriptError("Lubel", "Products Search", "Unauthorized", vehicle)
                print(script_error)
                raise script_error
            else:
                script_error = ScriptError("Lubel", "Products Search", f"{e.__str__()}", vehicle)
                print(script_error)
                raise script_error
        except Exception as e:
            script_error = ScriptError("Lubel", "Products Search", f"{e.__str__()}", vehicle)
            print(script_error)
            raise script_error