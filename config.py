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

    # [실험/기본 OFF] /route·/direction 진행상황으로 '지나온 노드'를 자동 추론해
    # /locate 에서 제외. ⚠️ 결함: 출발 노드(출입구)도 제외해 시작 위치를 못 잡음.
    # → 기본 OFF. 앱이 명시적 passed/exclude 를 보내는 방식(권장)이 이 플래그와
    #   무관하게 항상 동작하므로 그쪽을 사용. 켜려면 AUTO_EXCLUDE_PASSED=1.
    AUTO_EXCLUDE_PASSED = os.getenv("AUTO_EXCLUDE_PASSED", "0") == "1"

    TESTING = False


class TestConfig(Config):
    TESTING = True
    DATA_DIR = BASE_DIR / "tests" / "fixtures"
    AUTO_EXCLUDE_PASSED = False  # 테스트는 전역 진행상태 영향 받지 않도록
