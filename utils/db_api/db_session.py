import datetime
import logging
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from aiogram import types
from sqlalchemy.orm import Session
from data import config
from utils.db_api import models
from data import const, exceptions
from data.exceptions import UnknownBarcode


class DataBase:
    __factory = None

    def __new__(cls, *args, **kwargs):
        """Если к базе данных не было подключение, то соединяется к ней."""
        if cls.__factory is None:
            logging.info('Database connection.')
            conn_str = sa.engine.URL.create(
                "mssql+pyodbc",
                username=config.USER_DB,
                password=config.USER_DB_PASSWORD,
                host=config.HOST_DB,
                database=config.DB_NAME,
                query={
                    "driver": config.DB_DRIVER
                },
            )
            engine = sa.create_engine(conn_str, echo=False)
            engine.connect()
            cls.__factory = orm.sessionmaker(bind=engine)
            if config.CREATE_START_DATA:
                from data.db_class import SqlAlchemyBase

                SqlAlchemyBase.metadata.create_all(engine)
            logging.info('Database connection was successful.')
        return super().__new__(cls)

    async def get_new_users(self) -> int:
        date = datetime.datetime.now()

        with self.create_session() as session:
            session: Session
            count_new_users = session.query(models.Users).filter(
                models.Users.tgu_date_registration.between(
                    datetime.datetime(
                        year=date.year, month=date.month, day=date.day,
                    ), datetime.datetime(
                        year=date.year, month=date.month, day=date.day,
                        hour=23, minute=59, second=59
                    )
                )
            ).count()
        return count_new_users

    def update_errors(self):
        """Обновляет значения ошибок в таблице."""
        with self.create_session() as session:
            logging.info('Errors update started.')
            for error_id, text_id in const.ERRORS.items():
                db_error = session.query(models.Errors).filter(
                    models.Errors.tge_id == error_id
                ).first()
                if db_error is None:
                    error = models.Errors()
                    error.tge_id = error_id
                    error.tge_text = text_id
                    session.add(error)
            session.commit()
            logging.info('Errors update finished.')

    def get_token(self, bot_login: str) -> str:
        """Возвращает токен бота."""
        with self.create_session() as session:
            token = session.query(
                models.Config.tgc_token
            ).filter(models.Config.tgc_bot_login == bot_login).first()[0]
        return token

    def create_session(self) -> Session:
        """Создает новую сессию."""
        return self.__factory()

    async def get_config(self, login: str) -> models.Config:
        """Получить конфиг по логину бота."""
        with self.create_session() as session:
            db_config = session.query(models.Config).filter(
                models.Config.tgc_bot_login == login
            ).first()
        if db_config is None:
            raise ValueError(
                'Failed to get config. An invalid username was passed.'
            )
        return db_config

    async def get_admins(self) -> List[models.Users]:
        """Получить всех администраторов."""
        with self.create_session() as session:
            admins = session.query(models.Users).filter(
                models.Users.tgu_user_status == const.ADMIN
            ).all()
        return admins

    async def get_user(self, user_id: str) -> models.Users:
        """Получение пользователя по его id (telegram)."""
        with self.create_session() as session:
            user = session.query(models.Users).filter(
                models.Users.tgu_user_id == str(user_id)
            ).first()
        return user

    async def add_user(self, message: types.Message, data: dict):
        """Добавляет пользователя в базу данных."""
        tlg_user = message.from_user
        bot_me = await message.bot.get_me()
        phone_number = data['phone_number']
        with self.create_session() as session:
            bot_db = session.query(models.Config.tgc_id).filter(
                models.Config.tgc_bot_login == bot_me.username
            ).first()[0]
            logging.info(
                f'Started adding the user {tlg_user.username} to the database.'
            )
            new_user = models.Users()
            new_user.tgu_user_id = str(tlg_user.id)
            new_user.tgu_name = tlg_user.first_name
            new_user.tgu_surname = tlg_user.last_name
            new_user.tgu_phone = phone_number
            new_user.tgu_login = tlg_user.username
            new_user.tgu_chat_id = message.chat.id
            new_user.tgu_bot = bot_db
            session.add(new_user)
            session.commit()
            logging.info(
                f'The user {tlg_user.username} has been added to the database.'
            )

    async def get_data_barcode(self, barcode: str) -> str:
        """Получает данные из базы данных по штрих-коду и поставляет их
         в шаблон"""
        with self.create_session() as session:
            if config.TYPE_INSERT == 'str':
                insert_barcode = barcode
            elif config.TYPE_INSERT == 'int':
                try:
                    insert_barcode = int(barcode)
                except ValueError:
                    raise exceptions.UnknownBarcode()
            else:
                raise exceptions.InvalidTypeInsert(
                    f'Type insert: str, int (not {config.TYPE_INSERT}).'
                )
            data = session.execute(
                config.DATA_REQUEST,
                {'insert': insert_barcode}
            ).first()
            if data is None:
                raise UnknownBarcode()
        return config.RESPONSE_TEMPLATE.format(*data)

    async def create_log_entry(
            self, message: types.Message, error: int = None,
            path_photo: str = None
    ):
        """Добавляет запись в лог."""
        with self.create_session() as session:
            config_db = await self.get_config(config.BOT_LOGIN)
            log = models.Log()
            log.tgl_error = error
            log.tgl_user_id = message.from_user.id
            log.tgl_user_text = message.text
            log.tgl_bot = config_db.tgc_id
            log.tgl_photo = path_photo
            session.add(log)
            session.commit()


if __name__ == '__main__':
    DataBase()