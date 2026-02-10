import os
from dotenv import load_dotenv
import logging

#Load .env
load_dotenv()

class Config:
    #Flask mode
    DEBUG = os.getenv("FLASK_ENV") == "development"

    #Database settings
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    SSL = os.getenv("SSL", "disable")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?sslmode={SSL}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Logging
    LOG_LEVEL = getattr(logging, "INFO")