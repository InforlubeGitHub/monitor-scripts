import requests

from entities.error import ScriptError

class Lubel:
    def __init__(self, api_key):
        self.retries = 10
        self.api_key = api_key
        self.auth = None

    def run(self, vehicle: str) -> None:
        print("Iniciando busca no script Lubel")

        try:
            self.login()
            self.search(vehicle)
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

            print("Auth response: ", response_body["Jwt"])
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                script_error = ScriptError("Lubel", "Login", "Unauthorized", "")
                print(script_error)
                return script_error
            else:
                script_error = ScriptError("Lubel", "Login", f"{e.__str__()}", "")
                print(script_error)
                raise script_error
        except Exception as e:
            script_error = ScriptError("Lubel", "Login", f"{e.__str__()}", "")
            print(script_error)
            raise script_error

    def search(self, vehicle: str) -> None:
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

            print("Search response: ", response_body)
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                script_error = ScriptError("Lubel", "Search", "Unauthorized", vehicle)
                print(script_error)
                return script_error
            else:
                script_error = ScriptError("Lubel", "Search", f"{e.__str__()}", vehicle)
                print(script_error)
                raise script_error
        except Exception as e:
            script_error = ScriptError("Lubel", "Search", f"{e.__str__()}", vehicle)
            print(script_error)
            raise script_error