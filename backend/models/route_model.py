from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

# 路线主表
class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    agency_id = Column(Integer, ForeignKey("travel_agencies.id"), nullable=False)
    #

    # 路线和游客 中介表 这里写的是两边
    # tourist_routes = relationship("TouristRouteRelation", back_populates="route")
    tourist_routes = relationship("TouristRouteRelation", back_populates="route", cascade="all, delete-orphan", passive_deletes=True)

    # 和景点 一
    points = relationship("RouteSpot", back_populates="route", cascade="all, delete-orphan")
    # 和旅社 多
    agency = relationship("TravelAgency", back_populates="routes")

    #也许可以这样？
    guide_assignments=relationship("RouteGuide",back_populates="route")



# 路线景点表
class RouteSpot(Base):
    __tablename__ = "route_points"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    sequence = Column(Integer, nullable=False)

    # 和路线 多
    route = relationship("Route", back_populates="points")

