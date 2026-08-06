from dotenv import load_dotenv
load_dotenv()
import os

class Config:

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this_is_a_dev_secret_key"

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///joshim.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")

    # Paystack
    PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")

    # SMS (Termii)
    TERMII_API_KEY = os.environ.get("TERMII_API_KEY")

    # Session security
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # set True once you're serving over https
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB upload limit