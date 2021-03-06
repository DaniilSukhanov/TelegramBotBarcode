import datetime

import sqlalchemy as sa

from data import const
from data.db_class import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'TLG_Users'

    tgu_user_id = sa.Column(
        'tgu_UserID', sa.String(50),
        primary_key=True,
        nullable=False
    )
    tgu_bot = sa.Column(
        'tgu_Bot', sa.Integer,
        sa.ForeignKey('TLG_Config.tgc_ID'),
        nullable=False
    )
    tgu_login = sa.Column(
        'tgu_Login', sa.Text(50)
    )
    tgu_name = sa.Column(
        'tgu_FirstName', sa.Text(50)
    )
    tgu_surname = sa.Column(
        'tgu_LastName', sa.Text(50)
    )
    tgu_chat_id = sa.Column(
        'tgu_ChatID', sa.Text(50)
    )
    tgu_phone = sa.Column(
        'tgu_Phone', sa.Text(50)
    )
    tgu_user_status = sa.Column(
        'tgu_UserStatus', sa.Integer,
        default=const.REGISTERED_USER
    )
    tgu_date_registration = sa.Column(
        'tgu_DateRegistration', sa.DateTime,
        default=datetime.datetime.now
    )
