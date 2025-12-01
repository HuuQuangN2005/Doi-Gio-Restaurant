import os
import sys
from dotenv import load_dotenv, find_dotenv
from colorama import Fore, init

init(autoreset=True)

load_dotenv(find_dotenv())

class Configs():
    def __init__(self):
        self.SECRET_KEY: str = os.getenv("SECRET_KEY")

        # Database settings
        self.DATABASE_HOST: str = os.getenv("DATABASE_HOST")
        self.DATABASE_PORT: str = os.getenv("DATABASE_PORT")
        self.DATABASE_USER: str = os.getenv("DATABASE_USER")
        self.DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
        self.DATABASE_NAME: str = os.getenv("DATABASE_NAME")

    def validate(self):

        required = {
            "DATABASE_HOST": self.DATABASE_HOST,
            "DATABASE_PORT": self.DATABASE_PORT,
            "DATABASE_USER": self.DATABASE_USER,
            "DATABASE_PASSWORD": self.DATABASE_PASSWORD,
            "DATABASE_NAME": self.DATABASE_NAME,
        }
        missing = [key for key, val in required.items() if not val]
        if missing:
            print(Fore.RED + f"Missing environment variables: {', '.join(missing)}")
            sys.exit(1)


settings = Configs()
settings.validate()



