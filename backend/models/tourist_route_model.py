from sqlalchemy import Column, Integer, ForeignKey, String, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class TouristRouteRelation(Base):
    __tablename__ = "tourist_route"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tourist_id = Column(Integer, ForeignKey('tourists.id'), nullable=False)
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)
    signup_date = Column(TIMESTAMP, server_default=func.now())
    status = Column(Enum('待确认', '已确认', '已取消', name='status_enum'), default='待确认')

    #
    tourist = relationship("Tourist", back_populates="tourist_routes")
    route = relationship("Route", back_populates="tourist_routes")




