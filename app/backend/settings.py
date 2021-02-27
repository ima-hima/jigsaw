import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
TESTING = True

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
if TESTING:
    DB_NAME += '_test'

TEXAS_API_EMAIL = os.getenv('TEXAS_EMAIL')
TEXAS_API_PASSWORD = os.getenv('TEXAS_PASSWORD')
TEXAS_API_APP_TOKEN = os.getenv('TEXAS_APP_TOKEN')
TEXAS_API_SECRET_TOKEN = os.getenv('TEXAS_SECRET_TOKEN')
TEXAS_API_KEY = os.getenv('TEXAS_API_KEY')
TEXAS_API_SECRET_KEY = os.getenv('TEXAS_API_SECRET_KEY')
