import os

from dotenv import load_dotenv
import logging

from data import const


path = os.path.join(
    os.getcwd(), '.env'
)
if not os.path.exists(path):
    logging.warning(f'The generated path is not correct ({path}).')
    path = os.path.join(const.PATH_DIRECTORY_ENV, '.env')
load_dotenv(path)
try:
    USER_DB = os.environ['USER_DB']
    USER_DB_PASSWORD = os.environ['USER_DB_PASSWORD']
    HOST_DB = os.environ['HOST_DB']
    DB_NAME = os.environ['DB_NAME']
    DB_DRIVER = os.environ['DB_DRIVER']
    BOT_LOGIN = os.environ['BOT_LOGIN']
    DATA_REQUEST = os.environ['DATA_REQUEST']
    RESPONSE_TEMPLATE = os.environ['RESPONSE_TEMPLATE']
    CREATE_START_DATA = os.environ['CREATE_START_DATA']
    TYPE_INSERT = os.environ['TYPE_INSERT']
except KeyError:
    logging.error(
        'Failed to get data from environment variable. '
        'Perhaps the problem is not the correct path to the .env file. '
        f'Path: {path}'
    )
