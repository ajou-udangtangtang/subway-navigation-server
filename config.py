import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent


class Config:
    DATA_DIR = BASE_DIR / "data"

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "subway_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "subway")

    KNN_K = int(os.getenv("KNN_K", "5"))

    TESTING = False


class TestConfig(Config):
    TESTING = True
    DATA_DIR = BASE_DIR / "tests" / "fixtures"
