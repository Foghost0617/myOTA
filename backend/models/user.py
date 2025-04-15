from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.core.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # 存储加密后的密码
    role = Column(Integer, nullable=False)  # 1游客, 2导游, 3旅社, 4文旅局