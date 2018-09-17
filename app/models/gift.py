from sqlalchemy import Column
from sqlalchemy import Integer,String,Float,Boolean,ForeignKey,desc,func
from sqlalchemy.orm import relationship
from app.models.base import db,Base

from flask import current_app

from app.spider.yushu_book import YuShuBook



class Gift(Base):
    id=Column(Integer,primary_key=True)
    user=relationship('User')
    uid=Column(Integer,ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched=Column(Boolean,default=False)      #表示这本图书是否已赠送

    def is_yourself_gift(self,uid):             #鱼漂业务逻辑，自己不能给自己赠送
        return True if self.uid==uid else False

    @classmethod
    def get_user_gifts(cls,uid):    #获取当前用户的gift
        gifts=Gift.query.filter_by(uid=uid,launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls,isbn_list):
        from app.models.wish import Wish    #防止循环导入
        #根据传入的一组isbn,到Wish表中计算出某个礼物的Wish心愿数量
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):         #根据isbn取图书信息
        yushu_book=YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    #对象代表一个礼物，具体
    #类代表礼物这个事务，它是抽象，不是具体的“一个”
    @classmethod
    def recent(cls):   #最近的礼物，展示在首页
        #链式调用
        recent_gift=Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(      #因为create_time从base中继承，所以这里用Gift.create_time
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift