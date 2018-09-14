from sqlalchemy import Column
from sqlalchemy import Integer,String,Float,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import db,Base

class Gift(Base):
    id=Column(Integer,primary_key=True)
    user=relationship('User')
    uid=Column(Integer,ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched=Column(Boolean,default=False)