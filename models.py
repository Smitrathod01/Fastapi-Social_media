from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class Post_Model(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,default=True)
    created_at = Column(DateTime,server_default=func.now())

    creater_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    creator = relationship('User_Model')

    like = relationship('Like_Model')

class User_Model(Base):
    __tablename__  = "users"

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String,nullable=False,unique=True)
    username = Column(String,nullable=False)
    password = Column(String,nullable=False)

class Like_Model(Base):
    __tablename__ = "likes"

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    
    post = relationship("Post_Model")
    user = relationship("User_Model")

    
    