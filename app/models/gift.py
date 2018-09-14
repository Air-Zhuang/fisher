from sqlalchemy import Column
from sqlalchemy import Integer,String,Float,Boolean
from sqlalchemy.orm import relationship
from app.models.base import db

class Gift(db.Model):
    id=Column(Integer,primary_key=True)
    user=relationship('User')
    uid=Column(Integer)
    launched=Column(Boolean,default=False)