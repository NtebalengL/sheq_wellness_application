import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///sheq.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email (adjust with your SMTP settings)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
