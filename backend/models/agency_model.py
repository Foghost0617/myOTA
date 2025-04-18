# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from backend.core.database import Base
#
# class TravelAgency(Base):
#     __tablename__ = 'travel_agencies'
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 外键关联到 users 表的 id
#     agency_name = Column(String(100))
#     address = Column(String(255))
#
#     # 这里是关联关系，表示一个 TravelAgency 可以有多个 Route
#     routes = relationship('Route', back_populates='agency')
