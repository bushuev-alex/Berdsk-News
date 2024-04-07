import os
from dotenv import load_dotenv

load_dotenv()

DB_LOGIN = os.getenv('DB_LOGIN')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


DJ_SCRT_KEY = os.getenv('DJ_SCRT_KEY')
PARSER_CWD = os.getenv('PARSER_CWD')


# адрес сервера Яндекс-почты для всех один и тот же
EMAIL_HOST = os.getenv('EMAIL_HOST')
# порт smtp сервера тоже одинаковый
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')

# ваше имя пользователя, например, если ваша почта user@yandex.ru,
# то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_BOX = os.getenv('EMAIL_HOST_BOX')
# пароль от почты
EMAIL_PSWD = os.getenv('EMAIL_PSWD')


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = os.getenv('CELERY_ACCEPT_CONTENT')
CELERY_TASK_SERIALIZER = os.getenv('CELERY_TASK_SERIALIZER')
CELERY_RESULT_SERIALIZER = os.getenv('CELERY_RESULT_SERIALIZER')
