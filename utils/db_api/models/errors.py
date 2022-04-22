import sqlalchemy as sa

from data.db_class import SqlAlchemyBase


class Errors(SqlAlchemyBase):
    __tablename__ = 'TLG_Errors'

    tge_id = sa.Column(
        'tge_ID', sa.Integer,
        primary_key=True,
        nullable=False
    )
    tge_text = sa.Column(
        'tge_Text', sa.String(50),
        nullable=False
    )
