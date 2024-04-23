from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import datetime as dt
from sqlalchemy import Integer, Column, String, DateTime


class User(SqlAlchemyBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=True, unique=True)
    password_hashed = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    reg_date = Column(DateTime, default=dt.datetime.now)
    conversions = orm.relationship("Conversion", back_populates="user")

