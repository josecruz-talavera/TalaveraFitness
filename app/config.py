import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    PYTHONPATH = os.getenv("PYTHONPATH")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Other options
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
