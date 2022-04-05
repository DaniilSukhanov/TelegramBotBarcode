import sqlalchemy as sa
import datetime

from utils.db_api.db_session import SqlAlchemyBase


class Log(SqlAlchemyBase):
    __tablename__ = 'TLG_Log'

    tgl_id = sa.Column(
        'tgl_ID', sa.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    tgl_datetime = sa.Column(
        'tgl_DateTime', sa.DateTime,
        default=datetime.datetime.now,
        nullable=False
    )
    tgl_bot_id = sa.Column(
        'tgl_BotID', sa.Integer,
        sa.ForeignKey('TLG_Config.tgc_ID'),
        nullable=False
    )
    tgl_transaction_type = sa.Column(
        'tgl_TransactionType', sa.Integer,
        nullable=False
    )
    tgl_user_id = sa.Column(
        'tgl_UserID', sa.String(50),
        sa.ForeignKey('TLG_Users.tgu_UserID')
    )
    tgl_text = sa.Column(
        'tgl_Text', sa.Text(4000)
    )
