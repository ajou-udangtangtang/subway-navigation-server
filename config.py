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

    # [임시/시연] /route·/direction 진행상황으로 '지나온 노드'를 자동 추론해
    # /locate 에서 제외 (개찰구 지나도 개찰구 고정되는 문제 완화).
    # 앱이 명시적 passed/exclude 를 보내면 그게 우선. 끄려면 0.
    AUTO_EXCLUDE_PASSED = os.getenv("AUTO_EXCLUDE_PASSED", "1") == "1"

    TESTING = False


class TestConfig(Config):
    TESTING = True
    DATA_DIR = BASE_DIR / "tests" / "fixtures"
    AUTO_EXCLUDE_PASSED = False  # 테스트는 전역 진행상태 영향 받지 않도록
