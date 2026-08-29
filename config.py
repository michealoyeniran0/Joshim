import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:

    # =========================
    # SECURITY
    # =========================

    SECRET_KEY = os.environ.get("SECRET_KEY")

    # =========================
    # DATABASE
    # =========================

    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        # Render may provide a postgres:// URL.
        # SQLAlchemy expects postgresql://.
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )

        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    else:
        # Local development fallback
        SQLALCHEMY_DATABASE_URI = "sqlite:///joshim.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # EMAIL
    # =========================

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
    MAIL_DEFAULT_SENDER = (
        "JoshimEdu",
        os.environ.get("EMAIL_USER")
    )

    # =========================
    # PAYSTACK
    # =========================

    PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")

    # =========================
    # TERMII SMS
    # =========================

    TERMII_API_KEY = os.environ.get("TERMII_API_KEY")

    # =========================
    # SESSION SECURITY
    # =========================

    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = bool(os.environ.get("DATABASE_URL"))
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # =========================
    # UPLOAD LIMIT
    # =========================

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024