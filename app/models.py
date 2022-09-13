from sqlalchemy.orm import relationship

from .database import BASE
from sqlalchemy_utils import EmailType,PasswordType
from sqlalchemy import *

class POST(BASE):
    __tablename__="posts"
    post_id=Column(INTEGER, primary_key=True, nullable=False)
    post_title = Column(String, nullable=False)
    post_content = Column(VARCHAR, nullable=False)
    post_published = Column(BOOLEAN, server_default="TRUE", nullable=False)
    post_created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(INTEGER,ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    post_owner= relationship("USER")

class USER(BASE):
    __tablename__="users"
    user_id = Column(INTEGER, primary_key=True, nullable=False)
    user_email=Column(EmailType,nullable=False,unique=True)
    user_password=Column(String,nullable=False)
    user_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class LIKE(BASE):
    __tablename__="likes"
    like_user_id=Column(INTEGER,ForeignKey("users.user_id",ondelete="CASCADE"),primary_key=True)
    like_post_id=Column(INTEGER,ForeignKey("posts.post_id",ondelete="CASCADE"),primary_key=True)