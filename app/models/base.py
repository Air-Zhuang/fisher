from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy,BaseQuery
from sqlalchemy import Column,Integer,SmallInteger
from contextlib import contextmanager

from datetime import datetime

class SQLAlchemy(_SQLAlchemy):
    '''封装了事务回滚，之后只需使用with语句就可以调用了'''
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class Query(BaseQuery): #继承修改了原来的filter_by方法，每次查询status=1的信息，实现了软删除功能
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status']=1
        return super(Query,self).filter_by(**kwargs)

db=SQLAlchemy(query_class=Query)      #实例化SQLAlchemy，如果没有自定义继承类，query_class不用填写



class Base(db.Model):
    __abstract__=True                                       #告诉SQLAlchemy不需要创建这张表。不这么写SQLAlchemy会报找不到主键错误
    create_time=Column('create_time',Integer)               #不能在这里对create_time设置默认值，因为这里是类变量，每一次生成数据表实例这个值是不会变的
    status=Column(SmallInteger,default=1)

    def __init__(self):                                     #只要实例化任意一个模型，这个模型都会自动生成这个创建时间
        self.create_time=int(datetime.now().timestamp())

    def set_attrs(self,attrs_dict):                     #web.register
        for key,value in attrs_dict.items():
            if hasattr(self,key) and key!='id':
                setattr(self,key,value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):       #既然实现了软删除，删除方法也要写一下
        self.status=0