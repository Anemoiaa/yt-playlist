import os
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
DOTENV_FILE = os.path.join(BASE_DIR, '.env')


class Settings(BaseSettings):
    DELAY: float


settings = Settings(_env_file=DOTENV_FILE)
