import os
from dotenv import load_dotenv

load_dotenv()

secret_register_key = os.getenv('SECRET_REGISTER_KEY')


class SettingConnectDatabase:
    """Настройки подключения(создания url-адреса) к базе данных"""

    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.name = os.getenv("DB_NAME")

    @property
    def connection_string(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


connect_url = SettingConnectDatabase()
