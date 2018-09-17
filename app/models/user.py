from sqlalchemy import Column
from sqlalchemy import Integer,String,Float,Boolean

from app.libs.enums import PendingStatus
from app.models.base import db,Base

from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.drift import Drift
from app.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish

from math import floor

class User(UserMixin,Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password=Column('password',String(128),nullable=False)                #默认是=前作为数据库字段名，假如想自定义，需要传入字符串
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

    def can_send_drift(self):
        '''
        鱼豆必须足够(大于等于1)
        每索取两本书，自己必须送出一本书
        '''
        if self.beans<1:
            return False
        success_gifts_count=Gift.query.filter_by(uid=self.id,launched=True).count()
        success_receive_count=Drift.query.filter_by(requester_id=self.id,pending=PendingStatus.Success).count()
        return True if floor(success_receive_count/2)<=floor(success_gifts_count) else False

    def check_password(self,raw):       #完成login页面用户输入的明文密码和数据库的加密密码的比对
        return check_password_hash(self._password,raw)

    def can_save_to_list(self,isbn):    #是否可以将书放入到心愿清单
        if is_isbn_or_key(isbn)!='isbn':
            return False
        yushu_book=YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        #不允许一个用户同时赠送多本相同的图书
        #一个用户不可能同时成为赠送者和索要者

        #既不在赠送清单，也不在心愿清单才能添加
        gifting=Gift.query.filter_by(uid=self.id,isbn=isbn,launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    @property               #--->drift.send_drift
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter)+'/'+str(self.receive_counter)
        )

    def get_id(self):   #flask_login需要在model层返回一个标志id的函数，函数名固定
        return self.id

@login_manager.user_loader   #使之后每次调用时候的current_user变成一个用户模型
def get_user(uid):
    return User.query.get(int(uid))    #主键查新不需要用filter_by