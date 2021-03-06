import sqlalchemy as sa
import datetime

from data.db_class import SqlAlchemyBase


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
    tgl_bot = sa.Column(
        'tgl_Bot', sa.Integer,
        sa.ForeignKey('TLG_Config.tgc_ID'),
        nullable=False
    )
    tgl_user_id = sa.Column(
        'tgu_UserID', sa.String(50),
        sa.ForeignKey('TLG_Users.tgu_UserID')
    )
    tgl_user_text = sa.Column(
        'tgl_UserText', sa.Text(4096)
    )
    tgl_error = sa.Column(
        'tgl_Error', sa.Integer,
        sa.ForeignKey('TLG_Errors.tge_ID')
    )
    tgl_photo = sa.Column(
        'tgl_Photo', sa.String(250)
    )
