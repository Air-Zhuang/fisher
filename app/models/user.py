from sqlalchemy import Column
from sqlalchemy import Integer,String,Float,Boolean
from app.models.base import db,Base

from werkzeug.security import generate_password_hash,check_password_hash

class User(Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password=Column('password',String(128))                #默认是=前作为数据库字段名，假如想自定义，需要传入字符串
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,raw):
        self._password=generate_password_hash(raw)

    def check_password(self,raw):       #完成login页面up莽荒纪
        check_password_hash(self._password,raw)