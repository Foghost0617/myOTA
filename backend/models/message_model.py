from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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

    is_location = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # ✅ 新增这两列：代表“这个位置是谁的”
    location_owner_id = Column(Integer, nullable=True)
    location_owner_role = Column(Integer, nullable=True)

    group_receivers = relationship("GroupMessageReceiver", back_populates="message")


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


class GroupMessageReceiver(Base):
    __tablename__ = "group_message_receivers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger, ForeignKey("messages.id"), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    user_role = Column(Integer, nullable=False)

    # 关联回 Message（反向）
    message = relationship("Message", back_populates="group_receivers")