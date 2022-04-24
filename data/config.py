from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

USER_DB = env.str('USER_DB')
USER_DB_PASSWORD = env.str('USER_DB_PASSWORD')
HOST_DB = env.str('HOST_DB')
DB_NAME = env.str('DB_NAME')
DB_DRIVER = env.str('DB_DRIVER')
BOT_LOGIN = env.str('BOT_LOGIN')
DATA_REQUEST = env.str('DATA_REQUEST')
RESPONSE_TEMPLATE = env.str('RESPONSE_TEMPLATE')
CREATE_START_DATA = env.bool('CREATE_START_DATA')
