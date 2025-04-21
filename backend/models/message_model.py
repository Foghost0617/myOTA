from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, nullable=False)
    sender_role = Column(Integer, nullable=False)  # 1游客, 2导游, ...
    receiver_id = Column(Integer, nullable=False)
    receiver_role = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_group = Column(Boolean, default=False)
    is_read = Column(Boolean, default=False)

