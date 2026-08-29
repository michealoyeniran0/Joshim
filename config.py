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

    database_url = os.environ.get("DATABASE_URL")

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///joshim.db"

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

    PAYSTACK_SECRET_KEY = os.environ.get(
        "PAYSTACK_SECRET_KEY"
    )

    # =========================
    # TERMII
    # =========================

    TERMII_API_KEY = os.environ.get(
        "TERMII_API_KEY"
    )

    # =========================
    # TUTOR CONTACT
    # =========================

    TUTOR_WHATSAPP = os.environ.get(
        "TUTOR_WHATSAPP"
    )

    # =========================
    # SESSION SECURITY
    # =========================

    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = (
        os.environ.get("FLASK_ENV") == "production"
    )

    PERMANENT_SESSION_LIFETIME = timedelta(
        hours=2
    )

    # =========================
    # UPLOAD LIMIT
    # =========================

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024