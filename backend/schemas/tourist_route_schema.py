# 游客报名某条路线的请求数据结构
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TouristRouteCreate(BaseModel):
    tourist_id: int
    route_id: int
    status: Optional[str] = '待确认'  # 默认待确认状态

    class Config:
        from_attributes = True

# 后端返回的游客报名信息
class TouristRouteOut(BaseModel):
    id: int
    tourist_id: int
    route_id: int
    signup_date: datetime
    status: str

    class Config:
        from_attributes = True
