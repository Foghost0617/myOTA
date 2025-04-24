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

class ChatGroup(Base):
    __tablename__ = "chat_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_by_id = Column(Integer, nullable=False)
    created_by_role = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatGroupMember(Base):
    __tablename__ = "chat_group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("chat_groups.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    user_role = Column(Integer, nullable=False)
