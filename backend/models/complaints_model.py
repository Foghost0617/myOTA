from sqlalchemy import Column, Integer, Text, Enum, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    tourist_id = Column(Integer, ForeignKey("tourists.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum("未处理", "已处理", name="complaint_status"), default="未处理")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # 可选：建立游客的反向关系
    tourist = relationship("Tourist", back_populates="complaints")
