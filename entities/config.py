from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        self.lubel_api_key = None
        self.interval = None

    def load(self):
        try:
            load_dotenv()
            self.lubel_api_key = os.getenv("LUBEL_API_KEY")
            if not self.lubel_api_key:
                raise ValueError("LUBEL_API_KEY não encontrado nas variáveis de ambiente.")
            self.interval = int(os.getenv("INTERVAL", 2))  # Default to 1440 minutes if not set
        except Exception as e:
            print(f"Erro ao carregar variáveis de ambiente: {e}")
            raise

    def show(self):
        print(f"LUBEL_API_KEY: {self.lubel_api_key}")
        print(f"INTERVAL: {self.interval}")