from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
import datetime as dt
from sqlalchemy import Integer, Column, DateTime, ForeignKey


class Conversion(SqlAlchemyBase):
    __tablename__ = "conversions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=dt.datetime.now)
    user = orm.relationship("User")
