from enum import Enum

from pymysql import TIMESTAMP
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum
from sqlalchemy import TIMESTAMP
from sqlalchemy import Date  # 引入 Date 类型

class RouteGuide(Base):
    __tablename__ = "route_guides"

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    guide_id = Column(Integer, ForeignKey("guides.id", ondelete="CASCADE"), nullable=False)

    trip_start_time = Column(Date, nullable=True)  # 修改为 Date 类型
    trip_end_time = Column(Date, nullable=True)    # 修改为 Date 类型

    route = relationship("Route", back_populates="guide_assignments")
    guide = relationship("Guide", back_populates="assigned_routes")



