from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
USER_DB = env.str('USER_DB')
USER_DB_PASSWORD = env.str('USER_DB_PASSWORD')
HOST_DB = env.str('HOST_DB')
DB_NAME = env.str('DB_NAME')
DB_DRIVER = env.str('DB_DRIVER')

