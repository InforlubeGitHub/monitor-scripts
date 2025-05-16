from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        self.lubel_api_url = None
        self.mobil_api_url = None
        self.castrol_api_url = None
        self.totalenergies_api_url = None

        self.lubel_api_key = None
        self.mobil_api_key = None
        self.castrol_api_key = None
        self.totalenergies_api_key = None

        self.interval = None
        self.discord_webhook = None

    def load(self):
        try:
            load_dotenv()

            self.interval = int(os.getenv("INTERVAL", 2))

            #API KEYS
            self.lubel_api_key = os.getenv("LUBEL_API_KEY")
            if not self.lubel_api_key:
                raise ValueError("LUBEL_API_KEY não encontrado nas variáveis de ambiente.")

            self.mobil_api_key = os.getenv("MOBIL_API_KEY")
            if not self.mobil_api_key:
                raise ValueError("MOBIL_API_KEY não encontrado nas variáveis de ambiente.")

            self.castrol_api_key = os.getenv("CASTROL_API_KEY")
            if not self.castrol_api_key:
                raise ValueError("CASTROL_API_KEY não encontrado nas variáveis de ambiente.")

            self.totalenergies_api_key = os.getenv("TOTALENERGIES_API_KEY")
            if not self.totalenergies_api_key:
                raise ValueError("TOTALENERGIES_API_KEY não encontrado nas variáveis de ambiente.")

            self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
            if not self.discord_webhook:
                raise ValueError("DISCORD_WEBHOOK_URL não encontrado nas variáveis de ambiente.")

            #API URLS
            self.lubel_api_url = os.getenv("LUBEL_API_URL")
            if not self.lubel_api_url:
                raise ValueError("LUBEL_API_URL não encontrado nas variáveis de ambiente.")

            self.mobil_api_url = os.getenv("MOBIL_API_URL")
            if not self.mobil_api_url:
                raise ValueError("MOBIL_API_URL não encontrado nas variáveis de ambiente.")

            self.castrol_api_url = os.getenv("CASTROL_API_URL")
            if not self.castrol_api_url:
                raise ValueError("CASTROL_API_URL não encontrado nas variáveis de ambiente.")

            self.totalenergies_api_url = os.getenv("TOTALENERGIES_API_URL")
            if not self.totalenergies_api_url:
                raise ValueError("TOTALENERGIES_API_URL não encontrado nas variáveis de ambiente.")

        except Exception as e:
            print(f"Erro ao carregar variáveis de ambiente: {e}")
            raise

    def show(self):
        print(f"INTERVAL: {self.interval}")

        print(f"DISCORD_WEBHOOK_URL: {self.discord_webhook}")

        print(f"MOBIL_API_KEY: {self.mobil_api_key}")
        print(f"CASTROL_API_KEY: {self.castrol_api_key}")
        print(f"TOTALENERGIES_API_KEY: {self.totalenergies_api_key}")
        print(f"LUBEL_API_KEY: {self.lubel_api_key}")

        print(f"LUBEL_API_URL: {self.lubel_api_url}")
        print(f"MOBIL_API_URL: {self.mobil_api_url}")
        print(f"CASTROL_API_URL: {self.castrol_api_url}")
        print(f"TOTALENERGIES_API_URL: {self.totalenergies_api_url}")