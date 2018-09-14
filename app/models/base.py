from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,SmallInteger

db=SQLAlchemy()

class Base(db.Model):
    __abstract__=True   #不这么写SQLAlchemy会报找不到主键错误
    status=Column(SmallInteger,default=1)

    def set_attrs(self,attrs_dict):
        for key,value in attrs_dict.items():
            if hasattr(self,key) and key!='id':
                setattr(self,key,value)