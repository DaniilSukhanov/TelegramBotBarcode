import logging
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.orm import Session
from data import config
from utils.db_api import models
from data import const


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

            from data.db_class import SqlAlchemyBase

            SqlAlchemyBase.metadata.create_all(engine)
            logging.info('Database connection was successful.')
        return super().__new__(cls)

    def create_session(self) -> Session:
        """Создает новую сессию."""
        return self.__factory()

    def get_config(self, login: str) -> models.Config:
        """Получить конфиг по логину бота."""
        session = self.create_session()
        db_config = session.query(models.Config).filter(
            models.Config.tgc_bot_login == login
        ).first()
        if db_config is None:
            raise ValueError(
                'Failed to get config. An invalid username was passed.'
            )
        return db_config

    def get_admins(self) -> List[models.Users]:
        """Получить всех администраторов."""
        session = self.create_session()
        admins = session.query(models.Users).filter(
            models.Users.tgu_user_status == const.ADMIN
        ).all()
        return admins

    def get_user(self, user_id: str) -> models.Users:
        session = self.create_session()
        user = session.query(models.Users).filter(
            models.Users.tgu_user_id == user_id
        ).first()
        return user

    async def add_user(self, message: types.Message, state: FSMContext):
        session = self.create_session()
        tlg_user = message.from_user
        logging.info(
            f'Started adding the user {tlg_user.username} to the database.'
        )
        bot_me = await message.bot.get_me()
        phone_number = (await state.get_data()).get('phone_number')
        bot_db = session.query(models.Config.tgc_id).filter(
            models.Config.tgc_bot_login == bot_me.username
        ).first()[0]
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

    def get_data_barcode(self, barcode: str) -> str:
        session = self.create_session()
        data = session.execute(
            config.DATA_REQUEST,
            {'insert': barcode}
        ).first()
        return config.RESPONSE_TEMPLATE.format(*data)


if __name__ == '__main__':
    DataBase()