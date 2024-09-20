from sqlalchemy import Column, Integer, String,Text
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)

class Blog(Base):
    __tablename__="blogs"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    content=Column(Text)
