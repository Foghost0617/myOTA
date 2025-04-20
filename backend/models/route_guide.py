from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base

class RouteGuide(Base):
    __tablename__ = "route_guides"

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    guide_id = Column(Integer, ForeignKey("guides.id", ondelete="CASCADE"), nullable=False)

    route = relationship("Route", backref="guide_assignments")
    guide = relationship("Guide", backref="assigned_routes")