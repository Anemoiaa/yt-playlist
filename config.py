import os
from pathlib import Path

from pydantic import BaseSettings, FilePath

BASE_DIR = Path(__file__).resolve().parent
DOTENV_FILE = os.path.join(BASE_DIR, '.env')


class Settings(BaseSettings):
    DELAY: float
    MAX_DURATION: str
    KEY_WORDS_FILE: FilePath
    LINKS_FILE: FilePath


settings = Settings(_env_file=DOTENV_FILE)
