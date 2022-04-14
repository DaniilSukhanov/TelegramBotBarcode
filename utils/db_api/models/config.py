import sqlalchemy as sa

from data.db_class import SqlAlchemyBase


class Config(SqlAlchemyBase):
    __tablename__ = 'TLG_Config'

    tgc_id = sa.Column(
        'tgc_ID', sa.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    tgc_bot_login = sa.Column(
        'tgc_BotLogin', sa.String(50),
        nullable=False, primary_key=True
    )
    tgc_token = sa.Column(
        'tgc_Token', sa.String(50),
        nullable=False
    )
    tgc_password = sa.Column(
        'tgc_Password', sa.String(50)
    )
    tgc_path_photo = sa.Column(
        'tgc_PathPhoto', sa.String(250)
    )
    tgc_proxy_url = sa.Column(
        'tgc_ProxyUrl', sa.String(50)
    )
    tgc_proxy_port = sa.Column(
        'tgc_ProxyPort', sa.String(50)
    )
    tgc_proxy_login = sa.Column(
        'tgc_ProxyLogin', sa.String(50)
    )
    tgc_proxy_pass = sa.Column(
        'tgc_ProxyPass', sa.String(50)
    )
    tgc_proxy_expired = sa.Column(
        'tgc_ProxyExpired', sa.DateTime
    )
    tgc_proxy_exp_send_to_user_id = sa.Column(
        'tgc_ProxyExpSendToUserID', sa.Integer
    )