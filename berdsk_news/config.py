import os
from dotenv import load_dotenv

load_dotenv()

DB_LOGIN = os.getenv('DB_LOGIN')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
EMAIL_PSWD = os.getenv('EMAIL_PSWD')

DJ_SCRT_KEY = os.getenv('DJ_SCRT_KEY')
PARSER_CWD = os.getenv('PARSER_CWD')
