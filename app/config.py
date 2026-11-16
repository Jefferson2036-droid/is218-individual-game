"""Settings, read from environment variables (see .env.example)."""

import os

DEV_SECRET = "dev-only-secret-change-me-before-deploying-0123456789"


class Settings:
    def __init__(self):
        self.database_url = os.environ.get("DATABASE_URL", "sqlite:///./arena.db")
        self.secret_key = os.environ.get("SECRET_KEY", DEV_SECRET)
        self.token_minutes = int(os.environ.get("TOKEN_MINUTES", "720"))
        self.cookie_secure = os.environ.get("COOKIE_SECURE", "false").lower() == "true"


settings = Settings()
