from sqlalchemy import Column
from sqlalchemy import Integer,String,Float,Boolean
from app.models.base import db

class Gift(db.Model):
    id=Column(Integer,primary_key=True)
    launched=Column(Boolean,default=False)