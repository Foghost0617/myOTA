from pydantic import BaseModel
from typing import Optional




class GuideUpdate(BaseModel):
    guide_id:int
    guide_name: Optional[str]
    phone: Optional[str]
    agency_id: Optional[int]

class GuideOut(BaseModel):
    id: int
    user_id: int
    guide_name: Optional[str]
    phone: Optional[str]
    agency_id: Optional[int]

    class Config:
        from_attributes = True

# 获取所有旅社？
class TravelAgencyOut(BaseModel):
    id: int
    agency_name: Optional[str]
    address:Optional [str]

    class Config:
        from_attributes = True

# 通过导游id获取旅社id
class AgencyIdOut(BaseModel):
    agency_id: int

    class Config:
        orm_mode = True


# 找导游所带的游客
class TouristBasic(BaseModel):
    id: int
    tourist_name: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True