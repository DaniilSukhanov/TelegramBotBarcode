import logging

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from data import config


SqlAlchemyBase = dec.declarative_base()


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

            import models

            SqlAlchemyBase.metadata.create_all(engine)
            logging.info('Database connection was successful.')
        return super().__new__(cls)

    def create_session(self) -> Session:
        """Создает новую сессию."""
        return self.__factory()


