from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # 存储加密后的密码
    role = Column(Integer, nullable=False)  # 1游客, 2导游, 3旅社, 4文旅局

class Tourist(Base):
    __tablename__ = 'tourists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    tourist_name = Column(String(50))
    phone = Column(String(20))

    user = relationship("User", backref="tourist", passive_deletes=True)

class Guide(Base):
    __tablename__ = 'guides'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    guide_name = Column(String(50))
    phone = Column(String(20))
    agency_id = Column(Integer)

    user = relationship("User", backref="guide", passive_deletes=True)

class TravelAgency(Base):
    __tablename__ = 'travel_agencies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    agency_name = Column(String(100))
    address = Column(String(255))

    user = relationship("User", backref="agency", passive_deletes=True)
    routes = relationship("Route", back_populates="agency")


class GovAdmin(Base):
    __tablename__ = 'gov_admins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    admin_name = Column(String(100))
    region = Column(String(100))

    user = relationship("User", backref="gov_admin", passive_deletes=True)

