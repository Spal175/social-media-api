import email

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship
class Post(Base):

    __tablename__="posts"

    id= Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default="True")
    createdat = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner= relationship("users")

class users(Base):
    __tablename__="users"
    id= Column(Integer,primary_key=True,nullable=False) 
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    createdat = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

class Votes(Base):
    __tablename__="votes"
    post_id = Column('posts_id', Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column('users_id', Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
      