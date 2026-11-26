"""Application configuration loaded from environment variables."""
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "sahayak-secure-default-secret-key-2026")
    AES_ENCRYPTION_KEY = os.environ.get("AES_ENCRYPTION_KEY", "W3u8q9Z4t7y1A5d3F6h0J2l4N8p0R2v4")
    HOST = os.environ.get("HOST", "127.0.0.1")
    PORT = int(os.environ.get("PORT", "5000"))
    DEBUG = os.environ.get("FLASK_ENV", "development").lower() == "development"

    # MySQL 8.0 configuration
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "ai_scheme_sahayak")

    # Session & Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    PERMANENT_SESSION_LIFETIME = 86400 * 7  # 7 days

    # Supported Languages
    SUPPORTED_LANGUAGES = [
        "en", "hi", "bn", "mr", "ta", "te", "gu", "kn", "ml", "pa", "or"
    ]

    # Optional External AI API (fallback to local rule-based NLP is always guaranteed)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret-key-for-automated-suites"
    MYSQL_DATABASE = "ai_scheme_sahayak_test"
